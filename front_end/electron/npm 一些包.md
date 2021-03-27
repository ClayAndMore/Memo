###  安装 node-gyp



New to windows so this took a while... Here's what I did to get this working. Including node-gyp and electron rebuild in here as well just in case people are landing here to build native libraries for Electron in windows

1. Install latest LTS node for windows from https://nodejs.org/en/download/
2. Go to Add or Remove programs and uninstall any existing visual studio build tools
3. Open Powershell as Admin
4. Verify node version is latest `node --version`
5. Upgrade npm version `npm install -g npm`
6. Remove existing installations of windows build tools and node-gyp `npm uninstall -g windows-build-tools node-gyp yarn`
7. Go to C:\Users\username and remove existing `.windows-build-tools` and `.node-gyp` folders
8. Make sure electron builder is in your dev dependencies
9. Add `"postinstall": "electron-builder install-app-deps"` to your `package.json` `scripts` object

Install things

```sh
npm install --global --production windows-build-tools
npm install --global node-gyp
setx PYTHON $env:USERPROFILE\.windows-build-tools\python27\python.exe
npm config set python $env:USERPROFILE\.windows-build-tools\python27\python.exe
npm install --global yarn
yarn // native deps will be built properly after this step
```



https://github.com/nodejs/node-gyp#on-windows



### 安装 sqlite3

First, add a postinstall step in your package.json:

```
"scripts": {
   "postinstall": "install-app-deps"
   ...
}
```

and then install the necessary dependencies and build:

```sh
npm install --save-dev electron-builder
npm install --save sqlite3
npm run postinstall
```

最好下载 5.0.0版本（此时最新是5.0.2, 有https://github.com/mapbox/node-sqlite3/issues/1424）这样的问题。

`npm install --save sqlite3@5.0.0`



一个node的orm: https://github.com/demopark/sequelize-docs-Zh-CN





### selet2



```  js
window.$ = window.jQuery = require('jquery');
require('select2')();
$(document).ready(function() {

    // Initialize select2
    initailizeSelect2();
});

// Initialize select2
function initailizeSelect2() {

    $(".select2_el").select2({
        ajax: {
            url: "ajaxfile.php",
            type: "post",
            dataType: 'json',
            delay: 250,
            data: function(params) {
                console.log("ttt", params)
                return {
                    searchTerm: params.term // search term
                };
            },
            processResults: function(response) {
                return {
                    results: response
                };
            },
            cache: true
        }
    });
}
```

