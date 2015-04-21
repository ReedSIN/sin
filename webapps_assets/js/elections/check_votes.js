// Created by Will Jones, in April 2015


function Election(fieldset) {
    this.id = fieldset.getAttribute('election');
    this.ranks = $(fieldset).find('input.vote_rank');
    this.quorum = $(fieldset).find('input[name=quorum-' + this.id + ']');
    this.alertBox = $(fieldset).find('.alert');
    this.writeIn = $(fieldset).find('#writeinUser');

    this.checkRanksUnique = function() {
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

    this.checkQuorum = function() {
	// Returns either 'vote', 'quorum' or 'noquorum'
	return $(this.quorum).filter('input:checked').val()
    };

    this.alertMessage = function(message) {
	// Displays an alert message with an error
	console.log('alert message');
	$(this.alertBox).css('display', 'block');
	$(this.alertBox).html(message);
    };

    this.alertHide = function(message) {
	// Removes the error message
	$(this.alertBox).css('display', 'block');
    };

    // Setup functionality

    // Make it so voting is disabled when not choosing vote option
    $(this.quorum).click(
	{election : this},
	function() {
	    if (election.checkQuorum() != 'vote') {
		$(election.ranks).prop('disabled', true);
	    } else {
		$(election.ranks).prop('disabled', false);
	    }
	});

    // Make it watch for the ranks being the same
    $(this.ranks).click(
	{election : this},
	function() {
	    if (election.checkRanksUnique() == false) {
		election.alertMessage('No two candidates may have the same rank.');
	    } else {
		election.alertHide();
	    }
	})

    // Validate username of write-in candidates
    this.validateWriteIn = function(response) {
	// Receives response indicating
    }

    $(this.writeIn).keypress(function() {
	username = $(this.writeIn).val();
	check_user(username, this.validateWriteIn)
    })


}

var elections = new Array();

$(document).ready(function() {
// Put all code to be executed after page load here

var fieldsets = $('fieldset');


for (i=0; i < fieldsets.length; i++) {
    election = new Election(fieldsets[i]);
    elections.push(election);
}


});
