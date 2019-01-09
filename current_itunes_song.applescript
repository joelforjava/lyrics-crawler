# Modified version of the original, which is found here: https://gist.github.com/joshuaswilcox/7251527
if application "Spotify" is running and application "iTunes" is not running then
	tell application "Spotify"
		if player state is stopped then
			set display to "No Track Playing"
		else
			set track_artist to artist of current track
			set track_name to name of current track
			set track_duration to duration of current track
			set seconds_played to player position
			set state to ""
			if player state is paused then
				set state to "(Paused) "
			end if
			# Changed delimiter from " - " to " || " in order
			# for the get_lyric script to better parse out artist
			# and track name.
			set display to state & track_name & " || " & track_artist
		end if
	end tell
else if application "Spotify" is running and application "iTunes" is running then
	--Get current states of iTunes and Spotify
	tell application "iTunes" to set itunesState to (player state as text)
	tell application "Spotify" to set spotifyState to (player state as text)
	
	if (itunesState is "paused" or itunesState is "stopped") and spotifyState is "playing" then
		tell application "Spotify"
			if player state is stopped then
				set display to "No Track Playing"
			else
				set track_artist to artist of current track
				set track_name to name of current track
				set track_duration to duration of current track
				set seconds_played to player position
				set state to ""
				if player state is paused then
					set state to "(Paused) "
				end if
				
				set display to state & track_artist & " || " & track_name
			end if
		end tell
	else if itunesState is "playing" and (spotifyState is "paused" or spotifyState is "stopped") then
		tell application "iTunes"
			if player state is stopped then
				set display to "No Track Playing"
			else
				set track_artist to artist of current track
				set track_name to name of current track
				set track_duration to duration of current track
				set seconds_played to player position
				set state to ""
				if player state is paused then
					set state to "(Paused) "
				end if
				
				set display to state & track_artist & " || " & track_name
			end if
		end tell
	else if (itunesState is "paused" or itunesState is "stopped") and spotifyState is "paused" then
		set display to "No Track Playing"
	else
		set display to "Crazyman!!!!"
	end if
else if application "iTunes" is running and application "Spotify" is not running then
	tell application "iTunes"
		if player state is stopped then
			set display to "No Track Playing"
		else
			set track_artist to artist of current track
			set track_name to name of current track
			set track_duration to duration of current track
			set seconds_played to player position
			set state to ""
			if player state is paused then
				set state to "(Paused) "
			end if
			
			set display to state & track_artist & " || " & track_name
		end if
	end tell
else
	set display to "No music app is running"
end if