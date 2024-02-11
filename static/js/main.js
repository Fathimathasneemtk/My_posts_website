$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

$(document).ready(function () {
    $(document).on("click",".js-toggle-modal",function(e){
        e.preventDefault()
        console.log("clicked")
        $(".js-modal").toggleClass("hidden")
    })
    
    .on("click",".js-button",function(e){
        console.log("clicked")
        e.preventDefault()
        const text=$(".js-post-text").val().trim()
        if (!text.length){
            return false
        }
        
        const $btn=$(this)
        $btn.prop("disabled",true).text("Posting")
        $.ajax({
            type:"POST",
            url:$(".js-post-text").data("post-url"),
            data:{
                text:text,
            },
            success:(dataHtml)=>{
                $(".js-modal").addClass("hidden")
                $("#posts-container").prepend(dataHtml)
                $btn.prop("disabled",false).text("Create Post")
                $(".js-post-text").val(" ")
    
            },
            error:(error)=>{
                console.warn("Error")
                $btn.prop("disabled",false).text("Error")
            }
    
        })
    })
    .on("click",".js-follow",function(e){
        e.preventDefault();
        console.log("clicked")
        const action=$(this).attr("data-action")
        $.ajax({
            type:"POST",
            url:$(this).data("url"),
            data:{
                username:$(this).data("username"),
                action:action
            },
            success:(data)=>{
                console.log(data.wording)
                $(".js-follow-text").text(data.wording)
                if (action == "follow"){
                    $(this).attr("data-action","unfollow")
                }else{
                    $(this).attr("data-action","follow")
                }
                console.log(action)
    
            },
            error:(error)=>{
                console.warn("Error")
            }
        })
    })
    // Your existing JavaScript code here
});

