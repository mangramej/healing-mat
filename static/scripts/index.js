
document.querySelector('#cancel-btn').addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'none';
});

function openModal(id, title) {
    document.querySelector('.bg-modal').style.display = 'flex';
    document.getElementById('modal-trans-id').innerText = id;
    document.getElementById('modal-title').innerText = title;

    var action_src = "";
    if(title == 'TRANSACTION') {
        action_src += "/transaction/"
    } else if ('STAFF') {
        action_src += "/staff/"
    }

    action_src += id +"/delete"
    var form = document.getElementById('delete_trans_form');
    form.action = action_src;
}
