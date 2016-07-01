/**
 * Created by Patrik on 1. 7. 2016.
 */
var index = {};


index.setUp = function(){
    $('#next').click(function(){
        //var curPage = document.URI.split('/').splice(-1);
        var curPage = '0';
        try{
            var page = parseInt(curPage);
            //index.showNextPage(page);
            window.location.href = 'http://127.0.0.1:8000/1/comments/1/'
        }catch(e){
            console.log('Bad page in URI!');
            alert('Bad page in URI!');
        }
    });
}

//index.showNextPage = function(page){
//     $.ajax({
//        type: 'GET',
//        url: '/1/comments/1',
//        success: function(json){
//            if('comment_tree' in json) {
//                index.showNewComments(json.comment_tree);
//                alert('New comments!');
//            }
//        },
//        dataType: 'json'
//     });
//}
//
//index.showNewComments = function(comments){
//    console.log(comments);
//    $('#comments_tree').html('');
//    var new_comments = '';
//    for(var i = 0; i < comments.length; i++){
//        var c = comments[i];
//        console.log(c.body);
//        new_comments += '<li> ' + c.body + '</li>'
//            //'<li id="{{ comments[i].id }}" class="c" style="margin-left:{{ c.depth|add:c.depth }}em;">'
//    }
//    $('#comments_tree').html(new_comments);
//}

index.setUp();
