browser.runtime.onMessage.addListener((request, sender, sendResponse) =>{
    {

        var url = window.location.href
        if (url.search("://mail.qq.com/") > -1) {
            mainframe = document.querySelector("#mainFrame")
            b = mainframe.contentWindow.document
            subject = b.querySelector("#subject").innerHTML
            date = b.querySelector("#local-time-caption").innerText
            body = b.querySelector("#contentDiv").innerText

        }
        else if (url.search("://mail.163.com/") > -1){
            a = document.getElementsByClassName("tR0 frame-main")
            for (i=0;i<a.length;i++){
                if (a[i].style.display != "none"){
                    var num = i
                    break
                }
            }
            mainframe = a[num].getElementsByTagName("iframe")[0]
            subject = a[num].getElementsByClassName("nui-fIBlock py0")[0].innerText
            date = a[num].querySelector(".ow0").querySelectorAll(".hX0")[2].innerText
            b = mainframe.contentWindow.document
            body = b.getElementsByTagName("body")[0].innerText
        }
        if (subject.length > 0) {
        // 如果获取的值不为空则返回数据到 popup.js
            sendResponse({"subject": subject, "body": body, "date": date});
        } else {
            sendResponse("no data found!");
        }

    }
})



