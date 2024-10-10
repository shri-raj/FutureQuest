function nextSection(sectionNumber) {
    const currentSection = document.getElementById(`section-${sectionNumber - 1}`);
    const questions = currentSection.querySelectorAll('.question');
    let allAnswered = true;

    questions.forEach(question => {
        const radioButtons = question.querySelectorAll('input[type="radio"]');
        const answered = Array.from(radioButtons).some(radio => radio.checked);
        
        if (!answered) {
            allAnswered = false;
            question.classList.add('error'); // Optional: Add an error class to highlight unanswered questions
        } else {
            question.classList.remove('error'); // Remove error class if answered
        }
    });

    if (allAnswered) {
        // Hide current section and show the next section
        currentSection.classList.remove('active');
        const nextSection = document.getElementById(`section-${sectionNumber}`);
        nextSection.classList.add('active');
    } else {
        alert("Please answer all questions before proceeding.");
    }
}
