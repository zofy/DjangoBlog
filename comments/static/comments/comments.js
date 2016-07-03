/**
 * Created by Patrik on 1. 7. 2016.
 */
var index = {};

var ajax = {};


index.setUp = function () {
    index.movePage();
    index.vote();
}

index.getPage = function () {
    var uriList = window.location.href.split('/');
    return uriList.filter(i => i !== "").splice(-1);
}

index.movePage = function(event){
    $('#prev, #next').on('click', function(){
        if($(this).is('#next')) index.redirect(1);
        if($(this).is('#prev')) index.redirect(-1);
    });
}

index. redirect = function(direction){
    var curPage = index.getPage();
    try {
        var page = parseInt(curPage);
        window.location.href = 'http://127.0.0.1:8000/1/comments/' + (page + direction).toString() + '/';
    } catch (e) {
        console.log('Bad page in URI!');
        alert('Bad page in URI!');
    }
}

index.vote = function(){
    var id = $('#up').parent().parent().attr('id');
    $('#up, #down').on('click', function(){
        alert('Voting!');
        if($(this).is('#up')) ajax.vote(id, {'up_votes': 1});
        if($(this).is('#down')) ajax.vote(id, {'down_votes': 1});
    });
}

ajax.vote = function(id, data){
    $.ajax({
        type: 'POST',
        url: '/comments/' + id + '/',
        data: data,
        //data: {'player': $('#search').val(), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
        success: alert('Success!'),
        dataType: 'json'
    });
}

index.setUp();
