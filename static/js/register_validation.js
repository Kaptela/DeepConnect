$(window).on('load', function() {
    const next_btn = $('#next_btn'); // jQuery selector for the button
    const form = $('.required_forms_controls'); // jQuery selector for the form elements

    next_btn.on('click', function() {
        let allValid = true; // Flag to check if all fields are valid

        form.each(function() { // Iterate over each form element
            const elem = $(this); // Wrap the element in jQuery
            if (elem.val().trim() === '') { // Check if the field is empty
                this.reportValidity(); // Report validity using native DOM method
                allValid = false; // Set flag to false
                return false; // Break out of the .each() loop
            }
        });

        if (allValid) {
            $('#modal2').modal('show'); // Show the modal if all fields are valid
        }
    });
});