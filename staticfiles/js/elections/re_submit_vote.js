// NEED INPUT VALIDATION BEFORE THIS IS TRIGGERED!
function submit_vote() {

    var query = {};

    // Grab the election id - not totally necessary but oh well
    var election_id = document.getElementById('election_id').value;
    query['election'] = election_id;
    query['votes'] = new Array();

    // Grab all rows of the table
    var votes = document.getElementsByClassName('vote_info');

    // Loop through rows and construct the query dictionary
    for (var i = 0; i < votes.length; i++) {
	// Grab the vote
	var v = votes[i].children[0].children[0];
	// Find the rank
	var rank = parseInt(v.value);
	// If the rank is not empty, add to the array
	if (rank > 0 && rank <= v.max) {
	    var vote_dict = {};
	    // The username of the candidate
	    var cand = v.id;

	    // construct a vote dictionary
	    vote_dict['candidate'] = cand;
	    vote_dict['rank'] = rank;
	    // Place the vote in the query dict's array of votes
	    query['votes'].push(vote_dict);
	}
    }
    console.log(query['votes']);
    // Create the form that will send data to the submit_vote page
    var new_form = document.createElement('form');
    new_form.method = 'post';
    new_form.action = '/webapps/elections/re_submit_vote/';
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
	console.log("i is " + i + " right now...")
        // Grab the input tag for the vote                                   
        var v_input = votes[i].children[0].children[0];
        // Find the rank                      
        console.log("lookign at " + v_input.id + " right now");
        var rank = parseInt(v_input.value);
	console.log(v_input.id + " had a rank of " + rank + ".");
        // If the rank is not empty, add to the array                                                           
        if (rank > 0 && rank <= v_input.max) {
	    console.log("passed the condition");
            var vote_dict = {};
            // The username of the candidate                                                                    
            var cand = v_input.id;
            // construct a vote dictionary                                                                    
            vote_dict['candidate'] = cand;
            vote_dict['rank'] = rank;
            // Place the vote in the query dict's array of votes
	    console.log(vote_dict['candidate']);
	    console.log(vote_dict['rank']);
	} else {
	    console.log("did not pass condition")
	}
    }
}