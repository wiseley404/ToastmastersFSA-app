document.addEventListener('click', function(e) {
    if (e.target.classList.contains('submit-btn') && e.target.dataset.eval) {
        e.preventDefault();
        
        const eval_id = e.target.dataset.eval;
        const answers = [];
        const comments = {};
        
        // Récupère les réponses
        document.querySelectorAll(`input[type="radio"][data-eval="${eval_id}"]:checked`).forEach(radio => {
            answers.push({
                criteria_id: radio.dataset.criteria,
                profile_id: radio.dataset.profile,
                level_id: radio.value
            });
        });
        
        // Récupère les commentaires
        const promises = [];
        document.querySelectorAll(`.comment-btn[data-eval="${eval_id}"]`).forEach(btn => {
            const profile_id = btn.dataset.profile;
            promises.push(
                fetch(`/speechs/evaluations/get-comment/${eval_id}/${profile_id}/`)
                    .then(r => r.json())
                    .then(data => {
                        if (data.comment) {
                            comments[profile_id] = data.comment;
                        }
                    })
            );
        });
        
        Promise.all(promises).then(() => {
            fetch('/speechs/evaluations/submit/', {
                method: 'POST',
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
                body: JSON.stringify({
                    eval_id: eval_id,
                    answers: answers,
                    comments: comments
                })
            })
            .then(r => r.json())
            .then(data => location.reload());
        });
    }
});


document.addEventListener('click', function(e) {
    if (e.target.closest('.comment-btn')) {
        e.preventDefault();
        const btn = e.target.closest('.comment-btn');
        const eval_id = btn.dataset.eval;
        const profile_id = btn.dataset.profile;
        
        // Ouvre le popup avec textarea
        const html = `
            <div class="comment-popup">
                <h2>Ajouter un commentaire</h2>
                <textarea id="comment-text" placeholder="Entrez votre commentaire..."></textarea>
                <button class="save-comment-btn" data-eval="${eval_id}" data-profile="${profile_id}">Sauvegarder</button>
            </div>
        `;
        openPopup(html);
    }
});


document.addEventListener('click', function(e) {
    if (e.target.classList.contains('save-comment-btn')) {
        const eval_id = e.target.dataset.eval;
        const profile_id = e.target.dataset.profile;
        const comment = document.getElementById('comment-text').value;
        
        // Envoie au serveur
        fetch('/speechs/evaluations/save-comment/', {
            method: 'POST',
            headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
            body: JSON.stringify({
                eval_id: eval_id,
                profile_id: profile_id,
                comment: comment
            })
        })
        .then(r => r.json())
        .then(data => {
            const btn = document.querySelector(`.comment-btn[data-eval="${eval_id}"][data-profile="${profile_id}"]`);
            btn.innerHTML = '<i class="fa-solid fa-edit"></i>';
            btn.dataset.hasComment = "true";
            closePopup();
        });
    }
});


document.addEventListener('click', function(e) {
    if (e.target.closest('.comment-btn[data-has-comment="true"]')) {
        const btn = e.target.closest('.comment-btn');
        const eval_id = btn.dataset.eval;
        const profile_id = btn.dataset.profile;
        
        // Récupère le commentaire du serveur
        fetch(`/speechs/evaluations/get-comment/${eval_id}/${profile_id}/`)
            .then(r => r.json())
            .then(data => {
                const html = `
                    <div class="comment-popup">
                        <h2>Commentaire</h2>
                        <textarea id="comment-text">${data.comment || ''}</textarea>
                        <button class="update-comment-btn" data-eval="${eval_id}" data-profile="${profile_id}">Mettre à jour</button>
                    </div>
                `;
                openPopup(html);
            });
    }
});

document.addEventListener('click', function(e) {
    if (e.target.classList.contains('update-comment-btn')) {
        const eval_id = e.target.dataset.eval;
        const profile_id = e.target.dataset.profile;
        const comment = document.getElementById('comment-text').value;
        
        fetch('/speechs/evaluations/save-comment/', {
            method: 'POST',
            headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
            body: JSON.stringify({
                eval_id: eval_id,
                profile_id: profile_id,
                comment: comment
            })
        })
        .then(r => r.json())
        .then(data => closePopup());
    }
});