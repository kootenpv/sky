function toggle_src(element_id, pre_src) {
    pre = document.getElementById('pre_iframe_' + element_id);
    post = document.getElementById('post_iframe_' + element_id);
    console.log('pc ' + pre.className);
    if (pre.className == "open") {
        pre.className = "closed"
        post.className = "closed"
        pre.style.display = 'none';
        post.style.display = 'none';
    } else {
        pre.className = "open"
        post.className = "open"
        pre.src = pre_src;
        pre.style.display = 'inherit';
        post.style.display = 'inherit';
    }
}

function toggle_body(element_id) {
    body = document.getElementById('card-body-' + element_id);
    console.log(body.style);
    if (body.style.height == '60px' | !body.style.height) {
        body.style.height = '200px';
    } else {
        body.style.height = '60px';
    }

}

function toggle_json(element_id) {
    jsonbody = document.getElementById('json-body-' + element_id);
    console.log(jsonbody);
    if (jsonbody.className == "card-body open") {
        jsonbody.className = "card-body closed"
        jsonbody.style.display = 'none';
    } else {
        jsonbody.className = "card-body open"
        jsonbody.style.display = 'inherit';
    }
}
