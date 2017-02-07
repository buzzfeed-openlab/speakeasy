/* global jQuery */
(function ($) {'use strict';
    $('audio[controls]').before(function () {

        var song = this;
        song.controls = false;

        var player_box = document.createElement('div');

        var toggle_holder = document.createElement('div');
        $(toggle_holder).addClass('btn-group center-block row col-xs-12');


        var data_table = document.createElement('table');
        $(data_table).addClass('table table-condensed');

        var player = document.createElement('section');
        $(player).addClass('btn-group  center-block row  col-xs-12');

        var load_error = function () {
            // console.log('error');
            $(player_box).find('.btn').addClass('disabled');
            $(player_box).find('input[type="range"]').hide();
            $(player_box).find('.glyphicon-refresh').text('Error');
            $(player_box).find('.glyphicon-refresh').parent().attr('title', 'There was an error loading the audio.');
            $(player_box).find('.glyphicon-refresh').parent().tooltip('fixTitle');
            $(player_box).find('.glyphicon-refresh').removeClass('glyphicon glyphicon-refresh spin');
        }; // load_error

        var addPlay = function () {
            var play = document.createElement('button');
            $(play).addClass('btn btn-xs btn-default disabled playbutton-container');

            play.setPlayState = function (toggle) {
                $(play).removeClass('disabled');
                if (toggle === 'play') {
                    $(play).html('<i class="glyphicon glyphicon-play"></i>');
                    $(play).click(function () {
                        song.play();
                    });
                }
                if (!song.paused || toggle === 'pause') {
                    $(play).html('<i class="glyphicon glyphicon-pause"></i>');
                    $(play).click(function () {
                        song.pause();
                    });
                }
            }; // setPlayState

            // media events from the audio element will trigger rebuilding the play button
            $(song).on('play', function () {play.setPlayState('pause'); });
            $(song).on('canplay', function () {play.setPlayState('play'); });
            $(song).on('pause', function () {play.setPlayState('play'); });

            var timeout = 0;

            var loadCheck = setInterval(function () {
                if (!song.paused){
                    play.setPlayState('pause');
                    clearInterval(loadCheck);
                    return true;
                }
                if (isNaN(song.duration) === false) {
                    play.setPlayState('play');
                    clearInterval(loadCheck);
                    return true;
                }
                if (song.networkState === 3 || timeout === 100) {
                    // 3 = NETWORK_NO_SOURCE - no audio/video source found
                    console.log('No audio source was found or a timeout occurred');
                    load_error();
                    clearInterval(loadCheck);
                    return false;
                }
                timeout++;
            }, 100); // x milliseconds per attempt
            $(player).append(play);
        }; // addPlay


        var addTime = function () {
            var time = document.createElement('button');
            $(time).addClass('btn btn-xs btn-default');
            $(time).tooltip({'container': 'body', 'placement': 'right', 'html': true});

            time.twodigit = function (myNum) {
                return ('0' + myNum).slice(-2);
            }; // time.twodigit

            time.timesplit = function (a) {
                if (isNaN(a)) {
                    return '<i class="glyphicon glyphicon-refresh spin"></i>';
                }
                var hours = Math.floor(a / 3600);
                var minutes = Math.floor(a / 60) - (hours * 60);
                var seconds = Math.floor(a) - (hours * 3600) - (minutes * 60);
                var timeStr = time.twodigit(minutes) + ':' + time.twodigit(seconds);
                if (hours > 0) {
                    timeStr = hours + ':' + timeStr;
                }
                return timeStr;
            }; // time.timesplit

            time.showtime = function () {
                var position_title = 'Click to Reset<hr style="padding:0; margin:0;" />Position: ';
                var length_title = 'Click to Reset<hr style="padding:0; margin:0;" />Length: ';
                if (!song.paused) {
                    $(time).html(time.timesplit(song.currentTime));
                    // $(time).attr({'title': length_title + (time.timesplit(song.duration))});
                } else {
                    $(time).html(time.timesplit(song.duration));
                    // $(time).attr({'title': position_title  + (time.timesplit(song.currentTime))});
                }
                $(time).tooltip('fixTitle');
            }; // time.showtime

            $(time).click(function () {
                song.pause();
                song.currentTime = 0;
                time.showtime();
                $(time).tooltip('fixTitle');
                $(time).tooltip('show');
            }); // time.click

            $(time).tooltip('show');
            $(song).on('loadedmetadata', time.showtime);
            $(song).on('loadeddata', time.showtime);
            $(song).on('progress', time.showtime);
            $(song).on('canplay', time.showtime);
            $(song).on('canplaythrough', time.showtime);
            $(song).on('timeupdate', time.showtime);
            if (song.readyState > 0) {
                time.showtime();
            } else {
                $(time).html('<i class="glyphicon glyphicon-refresh spin"></i>');
            }
            $(player).append(time);
        }; // addTime





        var addPlayer = function () {
            if ($(song).data('play') !== 'off') {
                addPlay();
            }

            if ($(song).data('time') !== 'off') {
                addTime();
            }

            $(player_box).append(player);
        }; // addPlayer


        var fillPlayerBox = function () {
            addPlayer();
        }; // fillPlayerBox

        fillPlayerBox();
        $(song).on('error', function () {
            console.log("Error encountered after fillPlayerBox");
            load_error();
        });
        return player_box;
    });
})(jQuery);
