$(function () {
    $("#check").click(function () {
    // chrome.tabs.query可以通过回调函数获得当前活跃tab
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        // 取出当前标签页的 tag_id, 发送一个消息出去, 同时带上回调函数
            chrome.tabs.sendMessage(tabs[0].id, { action: "search" }, function (response) {
            	// 回调函数，把传回的信息渲染在popup.html上
                $("#text1")[0].value = response.subject
                $("#text2")[0].value = response.body
                date = response.date.match(/（.+?）/)

                if (date == null){
                    date = response.date.match(/\(.+?\)/)
                }
                data1 = {
                    data: JSON.stringify({
                    'subject': response.subject,
                    'body': response.body,
                        "date":date
                    }),
                 }
                $.ajax({
                    type: 'POST',
                    url: "http://127.0.0.1:5000/",
                    data: data1,
                    dataType: "json",
                    success: function (res) {
                        $("#text3")[0].value = res.res
                        $("#text4")[0].value = res.fishEmail
                        $("#text5")[0].value = res.email
                    },
                    error: function (res) {
                        $("#text3")[0].value = res.res
                        $("#text5")[0].value = res.email
                        $("#text4")[0].value = res.fishEmail
                    }
                })
            });
        });
    });
});
