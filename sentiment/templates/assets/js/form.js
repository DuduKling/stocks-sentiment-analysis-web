const toDateInputValue = (date) => {
    let local = new Date(date);
    local.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    return local.toJSON().slice(0,10);
};

let minDay = new Date();
minDay.setDate(minDay.getDate() - 6);

inputEndDate.value = toDateInputValue(new Date());
inputEndDate.max = toDateInputValue(new Date());
inputEndDate.min = toDateInputValue(minDay);

inputStartDate.value = toDateInputValue(new Date());
inputStartDate.max = toDateInputValue(new Date());
inputStartDate.min = toDateInputValue(minDay);

showLoading = () => {
    let loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'), { backdrop: 'static', keyboard: false })
    loadingModal.toggle()
}