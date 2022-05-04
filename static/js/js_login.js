let userList = {
    'LiuChenxu': 'Lcx123',
}


function reUserName() {
    let oText = oUserName.value;
    if (oText.length < 5) {
        oUserTips.innerHTML = '用户名至少为5位数';
        downBtn();
        return false;
    }
    clearTips();
    return true;
}

function reUserPwd() {
    let oText = oUserPwd.value;
    if (oText.length < 6) {
        oPwdTips.innerHTML = '密码至少为6位数';
        downBtn()
        return false;
    }
    if (oText.charCodeAt(0) < 'A'.charCodeAt(0) || oText.charCodeAt(0) > 'Z'.charCodeAt(0)) {
        oPwdTips.innerHTML = '密码首位必须是大写';
        downBtn();
        return false;
    }
    clearTips();
    return true;
}

function reAll() {
    if (reUserName() && reUserPwd()) {
        if (userList[oUserName.value] === oUserPwd.value) {
            alert('登录成功！')
            window.location.href = 'web/index.html';
        } else {
            alert('登录失败，请检查用户名或密码！')
        }
    } else {
        alert('有信息填写错误，请检查！')
    }
}

function clearTips() {
    oUserTips.innerHTML = '&nbsp;'
    oPwdTips.innerHTML = '&nbsp;'
}

function btn_able() {
    if (reUserName() && reUserPwd()) {
        oBtnLogin.className = "inp_bar btn_login text_bar";
        oBtnLogin.disabled = false;
    }
}

function downBtn() {
    oBtnLogin.className = 'inp_bar btn_login disabled';
    oBtnLogin.disabled = true;
}