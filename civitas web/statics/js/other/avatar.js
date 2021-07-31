function upload()
{
    var formData = new FormData();
    alert(document.getElementById('photoFile').files[0])
    formData.append("img",document.getElementById('photoFile').files[0]);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            document.getElementById("comment").innerHTML = xmlhttp.responseText;
		}
	}
    xmlhttp.open("POST","https://api.trickydeath.xyz/upload-avatar/",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.withCredentials = true;
    xmlhttp.send(formData);
}