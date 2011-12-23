#
# Sublime-CSSLint - https://github.com/martinkr/Sublime-CSSLint
#
# Validates your css-files every time you save it. The best part: a growl notification showing a summary of errors and warnings.
# Inspired by "Cross-Platform JSLint Support for Sublime Text Editor 2 (using NodeJS) by Eduardo A Lundgren Melo"
#
# Install
# - Copy files to your sublime-packages directory
# - Install node.js and npm: http://nodejs.org/#download (http://npmjs.org/ if necessary)
# - Install CSSLint using npm: npm install -g csslint
# - Install growl and growlnotify: http://growl.info/extras.php
#
# Sublime-CSSLint.sublime-settings
# - Set the locations of all three binaries
# - If necessary: set the  error and warning level. See: https://github.com/stubbornella/csslint/wiki/Rules
#
# @author Martin Krause public@mkrause.info
# @copyright Martin Krause (jquery.public.mkrause.info)
# @license MIT http://www.opensource.org/licenses/mit-license.php
# @license GNU http://www.gnu.org/licenses/gpl-3.0.html
#
# @requires node.js
#   http://nodejs.org/
#   https://github.com/joyent/node/wiki/Installation
#
# @requires CSSLint
#   http://csslint.net/
#   https://github.com/stubbornella/csslint
#
# @requires growlnotify
#  http://growl.info/extras.php
#

import os, re, subprocess, sublime, sublime_plugin

package = "Sublime-CSSLint"

class CSSLint(sublime_plugin.EventListener):

    settings =  sublime.load_settings(package + '.sublime-settings')

    def getPackageSetting(self,key):
      return self.settings.get(key)


    def growlNotify(self, result ,fileName):

      imgDir = os.path.join(sublime.packages_path(), package) + '/images/'

      if result.count('Error') > 0:
          image = 'error.png'
      else:
          image = 'success.png'

      a = []
      a.append('')
      a.append( str(result.count('Error') ) )
      a.append(' Errors, ')
      a.append( str(result.count('Warning') ) )
      a.append(' Warnings')
      title  =  ''.join(a)
      msg = fileName

      os.popen(self.getPackageSetting('pathGrowlNotify') +' -m \"%(msg)s\" -t \"%(title)s\" --image \"%(image)s\"'% {"msg": msg,"title":title,"image": imgDir + image} )


    def lint(self, path):
      result = subprocess.Popen(self.getPackageSetting('pathNode') +' '+ self.getPackageSetting('pathCSSLint')+' --format=compact '+self.getPackageSetting('rules'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      return ''.join(result.stdout.readlines())

    def on_post_save(self, view):
      fileName = view.file_name()
      result = re.search('\.(css)$', fileName )

      if result == None:
        return
      elif result.group(1) == 'css':
       self.growlNotify(self.lint( fileName ),fileName)
