
new Vue({
el: "#app",
data: {
    showAddSectionPopup: false,
    showEditSectionPopup: {},
    showAddBookPopup: {},
    currentDate: "",
},
created() {
    const d = new Date();
    const options = { day: "2-digit", month: "2-digit", year: "numeric" };
    this.currentDate = d.toLocaleDateString("en-GB", options);
},
methods: {
    toggleAddBookPopup(sectionId) {
    this.$set(
        this.showAddBookPopup,
        sectionId,
        !this.showAddBookPopup[sectionId]
    );
    },
    toggleEditSectionPopup(sectionId) {
    this.$set(
        this.showEditSectionPopup,
        sectionId,
        !this.showEditSectionPopup[sectionId]
    );
    },
},
});