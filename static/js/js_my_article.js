// 留言功能
function leaveMessage() {
    // 创建对应节点
    let oLi = document.createElement('li'),
        oSpan = document.createElement('span'), // 评论内容
        oDelA = document.createElement('a');  // 删除按钮
    // 设置a标签相应属性
    oDelA.href = 'javascript:void(0)';
    oDelA.innerHTML = '删除';
    oDelA.className = 'fr';
    // 删除功能
    oDelA.onclick = function () {
        oUl.removeChild(this.parentNode);
    }
    // 设置span标签相应属性
    oSpan.innerHTML = oText.value;
    oSpan.title = oText.value;
    // 将标签依次添加到li标签中
    oLi.append(oSpan)
    oLi.appendChild(oDelA);
    // 通过insertBefore将li标签插入到第一个元素位置。
    oUl.insertBefore(oLi, oUl.children[0]);
    // 清空文本框
    oText.value = '';
    // 初始化按钮
    oBtn.disabled = true;
    oBtn.className = "sub_comment";
}