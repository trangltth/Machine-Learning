let httpRequest

document.querySelector('#start_scrap').addEventListener('click', event => {
    Array.from(document.querySelector('#category').children).forEach(element => {
        if (element.selected === true){
            console.log(element)
            httpRequest = new XMLHttpRequest()
            httpRequest.onreadystatechange = function(){
                alter_result('product')
            };
            httpRequest.open('GET', 'scrap?category_id=' + element.value + '&category_name=' + element.textContent)
            httpRequest.send()
        }
    });

    document.querySelector('#loading').setAttribute('style', 'visibility:visible')
    document.querySelector('#scrap_category_list').remove()
})

document.querySelector('#scrap_one_category').addEventListener('click', event => {
    document.querySelector('#scrap_category_list').setAttribute('style','visibility:inline')
    document.querySelector('#scrapping_type').remove()

    
})

document.querySelector('#scrap_all_categories').addEventListener('click', event => {
    document.querySelector('#loading').setAttribute('style', 'visibility:visible')
    document.querySelector('#scrapping_type').remove()

    httpRequest = new XMLHttpRequest()
    httpRequest.onreadystatechange = function(){
        alter_result('category')
    };
    httpRequest.open('GET', 'scrap_all_categories')
    httpRequest.send()
})

function alter_result(type){
    if(httpRequest.readyState === XMLHttpRequest.DONE){
        if(httpRequest.status === 200){
            document.querySelector('#loading').remove()
            document.querySelector('#success_result').setAttribute('style', 'visibility:visible')
            response_content = JSON.parse(httpRequest.responseText)
            inserted_record = Number(response_content.inserted)
            updated_record = Number(response_content.updated)
            document.querySelector('#success_result > p').innerHTML = display_amount(inserted_record, type, 'is') + ' inserted'
                                                            + '<br>'    +  display_amount(updated_record, type, 'is') + ' updated'
                 
        }
        else{
            document.querySelector('#fail_result').setAttribute('style', 'visibility:visible')
        }
    }
}


// dynamic plural and singular unit
// dynamic verb
function display_amount(number, unit, verb = ''){
    result = ''

    if (number > 1){
        result = number + ' ' + plural_transform(unit) + ' ' + plural_transform(verb)
    }
    else {
        result = number + ' ' + unit + ' '+ verb
    }

    return result
}

//ToDo: how to know word is on plural or not?
// if implement, it will be text analysis -> to be update
function plural_transform(word){
    word_in_plural = ''
    irregular_rule = {child: 'children', goose: 'geese', man: 'men', woman: 'women',
                        tooth: 'teeth', mouse: 'mice', person: 'people', was:'were', is: 'are'}
    vowels = ['e', 'u', 'o', 'a', 'i']
    keep_word = ['sheep', 'series', 'species', 'deer']
    double_end = ['fez','gas']
    except_f_case = ['roof', 'belief', 'chef', 'chief']    
    except_o_case = ['photo', 'piano', 'halo']    
    es_case2 = ['ss','sh','ch']
    es_case1 = ['s', 'x', 'z']
    
    // In some cases, singular nouns ending in -s or -z, 
    // require that you double the -s or -z prior to adding the -es
        if(double_end.includes(word)){
            word_in_plural = word + word.slice(-1) + 'es'
        }
    // Some nouns don’t change at all when they’re pluralized.
        // sheep – sheep
        // series – series
        // species – species
        // deer –deer
        else if(keep_word.includes(word)){
            word_in_plural = word
        }
    // Plural Noun Rules for Irregular Nouns                
        // child – children
        // goose – geese    
        // man – men    
        // woman – women    
        // tooth – teeth    
        // foot – feet    
        // mouse – mice    
        // person – people 
        else if(Object.keys(irregular_rule).includes(word)){
            word_in_plural = irregular_rule[word]
        }
    // ends with ‑f or ‑fe, the f is often changed to ‑ve before adding the -s
        // Exceptions:
        // roof – roofs
        // belief – beliefs
        // chef – chefs
        // chief – chiefs
        else if(word.slice(-1) === 'f' & !(except_f_case.includes(word))){
            word_in_plural = word.slice(0,-1) + 'ves'
        }
        else if( word.slice(-2,) === 'fe'){
            word_in_plural = word.slice(0,-2) + 'ves'
        }
    //  noun ends in ‑y and the letter before the -y is a consonant, change the ending to ‑ies
        else if(word.slice(-1) === 'y' & !(vowels.includes(word.slice(-2)))){
            word_in_plural = word.slice(0,-1) + 'ies'
        }
    //  If the singular noun ends in ‑o, add ‑es 
        // Exceptions:
        // photo – photos
        // piano – pianos
        // halo – halos
        else if(word.slice(-1) === 'o' & !(except_f_case.includes(word))){
            word_in_plural = word + 'es'
        }

    // If the singular noun ends in ‑us, the plural ending is frequently ‑i.
        else if(word.slice(-2,) === 'us'){
            word_in_plural = word.slice(0,-2) + 'i'
        }
    // If the singular noun ends in ‑is, the plural ending is ‑es.
        else if(word.slice(-2,) === 'is'){
            word_in_plural = word.slice(0,-2) + 'es'
        }
    // If the singular noun ends in ‑on, the plural ending is ‑a.
        else if(word.slice(-2,) === 'on'){
            word_in_plural = word.slice(0,-2) + 'a'
        }
    // ‑s, -ss, -sh, -ch, -x, or -z, add ‑es
        else if (es_case2.includes(word.slice(-2,)) | es_case1.includes(word.slice(-1) )){
            word_in_plural = word + 'es'
        }    
    // If the singular noun ends in -y and the letter before the -y is a vowel, simply add an -s
    // add s
        else{
            word_in_plural = word + 's'
        }

    return word_in_plural
}

document.querySelector('#cancel_job').addEventListener('click', event => {
    console.log('cancel job');
    // httpRequest = new XMLHttpRequest()
    
    // httpRequest.onreadystatechange = function(){
    //     console.log('Cancel')
    // }
    // httpRequest.open('GET', 'cancel_job')
    // httpRequest.send()
    // console.log(document.querySelector('#loading_content').children[0])
    // document.querySelector('#loading_content').textContent = 
    // document.querySelector('#cancel_job').setAttribute('style', 'visibility:hidden')
})

