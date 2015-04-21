// NEED INPUT VALIDATION BEFORE THIS IS TRIGGERED!
function hideCandidates() {
//    document.getElementById('candidateTable').style.display = "none";
    vote_rows = document.getElementById("candidateTable").children[0]
	.getElementsByClassName("vote_info");
    for (var i = 0; i < vote_rows.length; i++) { 
	vote_rows[i].children[0].children[0].disabled = true; 
    }
    var writein = document.getElementById('writein');
    writein.children[0].children[0].disabled = true;
    writein.children[1].children[0].disabled = true;
}

function showCandidates() {
//    document.getElementById('candidateTable').style.display = "table";
    vote_rows = document.getElementById("candidateTable").children[0]
	.getElementsByClassName("vote_info");
    for (var i = 0; i < vote_rows.length; i++) { 
	vote_rows[i].children[0].children[0].disabled = false; 
    }
    writein.children[0].children[0].disabled = false;
    writein.children[1].children[0].disabled = false;

}

// checks if every element of an array is unique. 
function allUnique(array) {
    var counts = {};
    for (var i = 0; i < array.length; i++) {
	if (!counts[array[i].toString()]) {
	    counts[array[i].toString()] = 1;
	} else {
	    return false;
	}
    }
    return true;
}

// check if the ranks are o.k, i.e. none are equal. 
// also check if they are positive integers.
function validateRanks(query) {
    var ranks = [];
    for (var i = 0; i < query['votes'].length; i++) {
	ranks.push(query['votes'][i]['rank']);
    }

    var unique = (allUnique(ranks)) ? true : false;
    var positive = true;
    for (var i=0; i< ranks.length; i++) {
	if (ranks[i] < 0) { positive = false;}
    }
    return (unique && positive);
}

function submit_vote() {


    var query = {};

    // Grab the election id - not totally necessary but oh well
    var election_id = document.getElementById('election_id').value;
    var buttons = document.getElementById('quorumContainer');
    var bQuorum, didVote;
    didVote = buttons.children[0].checked;
    bQuorum = true;
    if (buttons.children[4].checked) {
	bQuorum = false;
    }
    query['election'] = election_id;
    query['votes'] = new Array();
    query['bQuorum'] = bQuorum;
    query['didVote'] = didVote;

    // Grab all rows of the table
    var votes = document.getElementsByClassName('vote_info');

    // Loop through rows and construct the query dictionary
    for (var i = 0; i < votes.length; i++) {
	// Grab the vote
	var v = votes[i].children[0].children[0];
	// Find the rank
	var rank = v.value;
	// If the rank is not empty, add to the array
	if (rank != 0 && rank <= v.max) {
	    var vote_dict = {};
	    // The username of the candidate
	    var cand = v.id;

	    // construct a vote dictionary
	    vote_dict['candidate'] = cand;
	    vote_dict['rank'] = rank;
	    vote_dict['isWritein'] = false;
	    // Place the vote in the query dict's array of votes
	    query['votes'].push(vote_dict);
	}
    }

    var writein = document.getElementById('writein');
    var wv = writein.children[0].children[0].value;

    // if writein has text in it, and it is not given a rank, 

    // check if the write-in candidate was given a rank.
    if (wv != 0) {
	writein_dict = {};
	writein_dict['rank'] = wv;
	writein_dict['candidate'] = writein.children[1].children[0].value;
	writein_dict['isWritein'] = true;
	query['votes'].push(writein_dict);
    }

    // Do validation if they voted
    if (didVote == true) {
	// validate the ranks (check if any are equal). 
	if (validateRanks(query) == false) {
	    alert("Sorry, but you can't give two candidates the same rank and all ranks must be positive integers. Please fix this and try submitting again.");
	    return;
	} 

	// validate the username of write-in candidate
	if (wv >0  && writein_dict['candidate'] != '') {
	    var cand_username = writein_dict['candidate'];
	    var xmlhttp;
	    if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	    } else {
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	    }
	    xmlhttp.open("GET",
			 "http://sin.reed.edu/webapps/elections/vote/check-username/?username=" 
			 + cand_username, false);
	    xmlhttp.send();
	    if (xmlhttp.responseText != "True") {
		alert("Username of write-in candidate not valid. Please double check this.");
		return;
	    }
	}
    }


    // Create the form that will send data to the submit_vote page
    var new_form = document.createElement('form');
    new_form.method = 'post';
    new_form.action = '/webapps/elections/submit_vote/'+election_id+'/';
    new_form.style.visibility = 'hidden';
    document.getElementById('vote-fieldset').appendChild(new_form);

    var query_string = JSON.stringify(query);
    var new_input = document.createElement('input');
    new_input.type = 'text';
    new_input.name = 'query_string';
    new_input.value = query_string;
    new_input.style.visibility = 'hidden';
    new_form.appendChild(new_input);
    new_form.submit();
}

// TESTER FUNCTION
function test() {
    var votes = document.getElementsByClassName('vote_info');

    for (var i = 0; i < votes.length; i++) {
        // Grab the input tag for the vote                                   
        var v_input = votes[i].children[0].children[0];
        // Find the rank                                                                
        var rank = v_input.value;
	console.log(v_input.max);
        // If the rank is not empty, add to the array                                                           
        if (rank > 0 && rank <= v_input.max) {
            var vote_dict = {};
            // The username of the candidate                                                                    
            var cand = v_input.id;
            // construct a vote dictionary                                                                    
            vote_dict['candidate'] = cand;
            vote_dict['rank'] = rank;
            // Place the vote in the query dict's array of votes
	    console.log(vote_dict['candidate']);
	    console.log(vote_dict['rank']);
	}
    }
}