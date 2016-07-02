/**
 * Created by Patrik on 1. 7. 2016.
 */
var index = {};


index.setUp = function () {
    index.nextPage();
    index.previousPage();
}

index.getPage = function () {
    var uriList = window.location.href.split('/');
    return uriList.filter(i => i !== "").splice(-1);
}

index.nextPage = function(){
    $('#next').click(function () {
        index.redirect(1);
    });
}

index.previousPage = function(){
    $('#prev').click(function () {
        index.redirect(-1);
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

index.setUp();
