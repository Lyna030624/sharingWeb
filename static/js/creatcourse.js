// 获得页面中所有折叠项目标题
var collapse = document.getElementById('collapse')
var title = collapse.getElementsByTagName('h3')
var content = collapse.getElementsByTagName('div')
// 通过循环绑定标题鼠标单击事件
for (var i = 0; i < title.length; i++) {
  title[i].addEventListener('click', function () {
    // 获取当前折叠项的内容窗口元素
    var current = this.nextElementSibling
    // 通过切换当前折叠项的display属性值为block来显隐当前折叠项的内容
    if (current.style.display == 'block') {
      current.style.display = 'none'
      this.className = ''
    } else {
      // 重置所有折叠项内容为隐藏
      for (var i = 0; i < content.length; i++) {
        content[i].style.display = 'none'
        content[i].previousElementSibling.className = ''
      }
      current.style.display = 'block'
      this.className = 'active'
    }
  })
}

var xhr
if (window.XhrRequest) {
  //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
  xhr = new XhrRequest()
}else {
  // IE6, IE5 浏览器执行代码
  xhr = new ActiveXObject('Microsoft.XHR')
}
xhr.onreadystatechange = function () {
  if (xhr.readyState == 4 && xhr.status == 200) {
    codeName = JSON.parse(xhr.responseText)
    for (i in codeName) {
      if (codeName[i].code.length == 2) {
        province.add(new Option(codeName[i].name, codeName[i].code, null, null))
      }
    }
  }
}


  function showpopup(){
    var overlay = document.getElementById("overlay");
    overlay.style.display = "block";
	
	   

  }

  function hidepopup(){
    var overlay = document.getElementById("overlay");
    overlay.style.display = "none";
  	
  }


