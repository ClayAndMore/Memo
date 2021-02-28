### Electron failed to install correctly, please delete node_modules/electron and try installing again

1、$ npm install electron-fix -D

2、Edit file ‘package.json’
"scripts": {
"fix": "electron-fix start"
}

3、npm run fix

然后再npm start