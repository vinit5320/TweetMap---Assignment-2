/**
 * Created by vinit. on 4/22/17.
 */

var map = null;
var elasticIndex = "tweetmap";
var elasticDocType = "tweets";
var marker = null;
var tweetID = [];
var searchQuery = "";

function plotData(response) {
    if(response) {
        $('#tweetInfo').show();
        document.getElementById('searchedTweets').innerHTML = ""+response["hits"]["total"];
        var data = response["hits"]["hits"];

        data.forEach(function (index) {
            var singleEntry = index["_source"];
            if(tweetID.indexOf(index['_id']) === -1 ) {

                tweetID.push(index['_id']);
                var sentiment = "" + singleEntry['sentiment'];
                var iconLink = (sentiment === '2') ? 'images/green.png' : ((sentiment === '1') ? 'images/yellow.png' : 'images/red.png');

                marker = new google.maps.Marker({
                    position: singleEntry['location'],
                    map: map,
                    icon: iconLink,
                    animation: google.maps.Animation.DROP
                });
                marker.addListener('click', function () {
                    showCard(singleEntry);
                });
            }
        });

        searchSpecific(searchQuery);
    }
}

function showCard(singleEntry) {
    $('#tweetDetail').show();
    document.getElementById('tweetText').innerHTML = singleEntry['tweet'] + " by <b>"+singleEntry['username']+"</b>";
}

function initMap() {

    $('#tweetInfo').hide();
    $('#tweetDetail').hide();

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: {lat: 39.0550557, lng: 4.0322128}
    });
}



function searchSpecific(searchTextValue) {

    if(searchQuery !== searchTextValue) {
        $('#tweetInfo').hide();
        $('#tweetDetail').hide();
        searchQuery = searchTextValue;
        document.getElementById('searchMenuText').innerHTML = searchTextValue+'<span class="caret"></span>';
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 3,
            center: {lat: 39.0550557, lng: 4.0322128}
        });
    }

    var xhr = new XMLHttpRequest();
    var url = "https://search-twittermap-zhychepoqowvbu7g3v5r7uqesq.us-west-2.es.amazonaws.com/"+elasticIndex+"/"+elasticDocType+"/_search/?size=1000&from=0&q=tweet:"+searchQuery;

    xhr.open("GET", url, true);

    xhr.onreadystatechange = function () {//Call a function when the state changes.
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                plotData(response);
            }
            else {
                alert('Error '+xhr.status);
            }
        }

    };
    xhr.send();
}