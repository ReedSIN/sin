// Created by Will Jones, in April 2015
// -----------------------------------------------------------------------------

function Election(fieldset) {
    this.id = fieldset.getAttribute('election');
    this.ranks = $(fieldset).find('input.vote_rank');
    this.quorum = $(fieldset).find('input[name=quorum-' + this.id + ']');
    this.alertBox = $(fieldset).find('.alert');
    this.writeIn = $(fieldset).find('#writeinUser');

    // Setup functionality

    // Make it so voting is disabled when not choosing vote option
    $(this.quorum).click({election : this}, toggleVoteDisabled);

    // Make it watch for the ranks being the same
    $(this.ranks).click({election : this}, toggleRankWarning);

    // Send request checking if valid username
    $(this.writeIn).keydown({election : this}, sendUsernameRequest);

    // Prevent text input in rank field
    $(this.ranks).on('change keyup', function() {
	// Remove invalid characters
	var sanitized = $(this).val().replace(/[^0-9]/g, '');
	// Update value
	$(this).val(sanitized);
    });
};

Election.prototype.checkRanksUnique = function() {
    // Makes sure no two candidates have the same rank
    var ranks = new Array()
    for (i=0; i < this.ranks.length; i++) {
	var value = parseInt(this.ranks[i].value);
	if (value != '') {
            ranks.push(value);
	}
    }
    ranks.sort();
    for (i = 1; i < ranks.length; i++) {
	if (ranks[i] == ranks[i-1]) {
            return false;
	}
    }
    return true;
};

Election.prototype.checkQuorum = function() {
    // Returns either 'vote', 'quorum' or 'noquorum'
    return $(this.quorum).filter('input:checked').val()
};

Election.prototype.alertMessage = function(message) {
    // Displays an alert message with an error
    $(this.alertBox).css('display', 'block');
    $(this.alertBox).html(message);
};

Election.prototype.alertHide = function(message) {
    // Removes the error message
    $(this.alertBox).css('display', 'none');
};


Election.prototype.toggleVoteDisabled = function(event) {
    var election = event.data.election
    if (election.checkQuorum() == 'quorum') {
	$(election.ranks).prop('disabled', true);
	$(election.ranks).attr('placeholder', "quorum")
    }
    else if(election.checkQuorum() == 'noquorum'){
	$(election.ranks).prop('disabled', true);
	$(election.ranks).attr('placeholder', "no quorum")
    }
    else {
	$(election.ranks).prop('disabled', false);
	$(election.ranks).attr('placeholder', "")
    }
}


Election.prototype.toggleRankWarning = function(event) {
    var election = event.data.election
    if (election.checkRanksUnique() == false) {
	election.alertMessage('No two candidates may have the same rank.');
    } else {
	election.alertHide();
    }
}

// Validate username of write-in candidates
Election.prototype.validateWriteIn = function(response, election) {
    // Receives response indicating whether write-in username
    // is valid and changes color of write-in input accordingly
    var blank = $(election.writeIn).val() == '';
    if (response['valid'] || blank) {
	$(election.writeIn).parent().removeClass('has-error');
	$(election.writeIn).parent().addClass('has-success');
    } else {
	$(election.writeIn).parent().removeClass('has-success');
	$(election.writeIn).parent().addClass('has-error');
    }
}


Election.prototype.sendUsernameRequest = function(event) {
    // Need to wait a bit so we aren't grabbing the input
    // before it is in the field
    setTimeout(function() {
	var election = event.data.election;
	var username = $(election.writeIn).val();
	check_user(username, election, election.validateWriteIn);
    }, 100);
}

Election.prototype.checkWriteIn = function() {
    // If there isn't a write in, return true
    if (this.writeIn.length == 0) {
        return true;
    }
    // Otherwise get username
    var username = $(this.writeIn).val();
    if (username == '') {
        return true;
    }
    var election = this;

    var result = check_user2(username);

    if (result['valid'] == false) {
	alert('Invalid write-in candidate!');
	return false;
    }
    return true;

}


// Putting elections in global scope
var elections = new Array();

function validateVotes() {
  // Stops the submission of the votes if there are any problems with the
  // persons votes.
  for (var i=0; i < elections.length; i++) {
    // Check the ranks
    if (!elections[i].checkRanksUnique()) {
	console.log('election ' + i + ' has identical ranks.')
      return false;
    }
  // Check the write-in candidates
    if (!elections[i].checkWriteIn()) {
	console.log('election ' + i + ' has an invalid write in')
      return false;
    }
  }
    return true
}


$(document).ready(function() {
// Put all code to be executed after page load here

  var fieldsets = $('fieldset');


  for (i=0; i < fieldsets.length; i++) {
      var election = new Election(fieldsets[i]);
      elections.push(election);
  }

});
