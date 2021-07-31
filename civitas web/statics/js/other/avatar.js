/*
上传头像
click_upload_avatar：模拟点击隐藏的上传按钮
upload_avatar：ajax上传头像
*/

function click_upload_avatar()
{
    document.getElementById("upload_avatar").click();
}

function upload_avatar()
{
    var formData = new FormData();
    formData.append("img",document.getElementById('upload_avatar').files[0]);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText;
            var json_str = JSON.parse(str);
            document.getElementById("tips").innerHTML = json_str["message"];
		}
	}
    xmlhttp.open("POST","https://api.trickydeath.xyz/upload-avatar/",true);
    xmlhttp.withCredentials = true;
    xmlhttp.send(formData);
}