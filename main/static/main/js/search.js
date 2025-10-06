let check = false

function search(){
    let input = document.querySelector('#search')
    let btn = document.querySelector('#search__btn')
    if(check === false){
        input.classList.remove('hide')
        btn.classList.remove('hide')
        check = true
    }
    else{
        input.classList.add('hide')
        btn.classList.add('hide')
        check = false
    }
}