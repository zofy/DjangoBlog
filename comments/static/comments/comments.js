/**
 * Created by Patrik on 1. 7. 2016.
 */
var index = {};

var ajax = {};


index.setUp = function () {
    index.movePage();
    index.vote();
    index.createComment();
    index.reply();
}

index.getIdAndPage = function () {
    var uriList = window.location.href.split('/').filter(i => i !== "");
    return [uriList.splice(uriList.length-3,uriList.length-4)[0], uriList.splice(-1)[0]];
}

index.movePage = function(event){
    $('#prev, #next').on('click', function(){
        if($(this).is('#next')) index.redirect(1);
        if($(this).is('#prev')) index.redirect(-1);
    });
}

index. redirect = function(direction){
    var curPage = index.getIdAndPage()[1];
    try {
        var page = parseInt(curPage);
        window.location.href = 'http://127.0.0.1:8000/1/comments/' + (page + direction).toString() + '/';
    } catch (e) {
        console.log('Bad page in URI!');
        alert('Bad page in URI!');
    }
}

index.vote = function(){
    $('#up, #down').on('click', function(){
        console.log('Voting!');
        var id = $(this).parent().parent().attr('id');
        if($(this).is('#up')) ajax.vote(id, {'up_votes': 1});
        if($(this).is('#down')) ajax.vote(id, {'down_votes': 1});
    });
}

index.getCommentPosition = function(li_id){
    for(var i = 0; i < $('ul li').length; i++){
        if(li_id === $($('ul li').get(i)).attr('id')) return i;
    }
    return null;
}

index.createComment = function(){
    $('.container').on('keypress', '.newComment', function(event){
        if (event.which === 13){
            console.log('Creating a new comment!');
            var idAndPage = index.getIdAndPage(), data = {'body': $(this).val()}, classList = this.classList;
            if(classList.length === 2){
                data['parent'] = classList[1];
            }
            ajax.createComment(idAndPage, data);
            $(this).val('');
        }
    });
}

index.reply = function(){
    $('.reply').on('click',  function(){
        var parent = $(this).parent().parent();
        var oldHtml = parent.html(), parent_id = $(parent).attr('id');
        var newHtml = '<div class="ui form">' +
                        '<div class="field">' +
                            '<input class="newComment ' + parent_id + '" type="text" placeholder="Join the discussion..">' +
                        '</div>' +
                       '</div>';
        parent.html(oldHtml + newHtml);
        console.log($('#' + parent_id + ' .ui.form'));
        $('#' + parent_id + ' .ui.form').toggleClass('hide');
    });
}

ajax.vote = function(id, data){
    $.ajax({
        type: 'PUT',
        url: '/comments/' + id + '/',
        data: data,
        success: function(json){alert('up: ' + json['up'] + '\n' + 'down: ' + json['down'] + '\n' + 'path: ' + json['path']); document.location.reload(true)},
        dataType: 'json'
    });
}

ajax.createComment = function(idAndPage, data){
    $.ajax({
        type: 'POST',
        url: '/' + idAndPage[0] + '/comments/' + idAndPage[1] + '/',
        data: data,
//        success: function(json){alert('Comment: ' + json['body'])},
        success: location.reload(),
        dataType: 'json'
    });
}

index.setUp();
