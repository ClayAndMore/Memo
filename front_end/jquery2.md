取消异步设置：

```js
$.ajax({
  url: myUrl,
  dataType: 'json',
  async: false,
  data: myData,
  success: function(data) {
    //stuff
    //...
  }
});
```

或：

```js
$.ajaxSetup({
async: false
});

$.getJSON(myUrl, myData, function(data) { 
  //stuff
  //...
});
```