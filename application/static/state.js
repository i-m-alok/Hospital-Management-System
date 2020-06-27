
function populate(s1, s2) {
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    s2.innerHTML = "";
    if (s1.value == "chandigarh") {
        var optionarray = ["chandigarh|Chandigarh"];
    }
    else if (s1.value == "Delhi") {
        var optionarray = ["New Delhi|New Delhi", "North Delhi|North Delhi", "North West Delhi|North West Delhi", "West Delhi|West Delhi", "South West Delhi|South West Delhi", "South Delhi|South Delhi", "South East Delhi|South East Delhi", "Central Delhi|Central Delhi",
            "North East Delhi|North East Delhi", "Shahdara|Shahdara", "East Delhi|East Delhi"];
    }
    else if (s1.value == "Haryana") {
        var optionarray = ["Ambala|Ambala", "Bhiwani|Bhiwani", "Charkhi Dadri|Charkhi Dadri", "Faridabad|Faridabad", "Fatehabad|Fatehabad", "Gurugram|Gurugram (Gurgaon)", "Hisar|Hisar"];
    }
    else if (s1.value == "Himachal Pradesh") {
        var optionarray = ["Bilaspur|Bilaspur", "Chamba|Chamba", "Hamirpur|Hamirpur", "Kangra|Kangra", "Kinnaur|Kinnaur", "Kullu|Kullu"];
    }
    else if (s1.value == "Jammu and Kashmir") {
        var optionarray = ["Jammu|Jammu", "Srinagar|Srinagar", "Anantnag|Anantnag", "Baramula|Baramula", "Kathua|Kathua"];
    }
    else if (s1.value == "Ladakh") {
        var optionarray = ["Leh|Leh", "Kargil|Kargil"];

    }
    else if (s1.value == "Punjab") {
        var optionarray = ["Mohali|Mohali", "Patiala|Patiala", "Tarn Taran|Tarn Taran", "Bathinda|Bathinda"];

    }
    else if (s1.value == "Rajasthan") {
        var optionarray = ["Ajmer|Ajmer", "Alwar|Alwar", "Banswara|Banswara", "Baran|Baran", "Barmer|Barmer", "Bharatpur|Bharatpur"];
    }
    else if (s1.value == "Rajasthan") {
        var optionarray = ["Ajmer|Ajmer", "Alwar|Alwar", "Banswara|Banswara", "Baran|Baran", "Barmer|Barmer", "Bharatpur|Bharatpur"];
    }
    else if (s1.value == "Uttarakhand") {
        var optionarray = ["Nainital|Nainital", "Dehradun|Dehradun", "Uttarkashi|Uttarkashi", "Haridwar|Haridwar"];
    }
    else if (s1.value == "Uttarpradesh") {
        var optionarray = ["Agra|Agra", "Aligarh|Aligarh", "Allahabad|Allahabad", "Ambedkar Nagar|Ambedkar Nagar", "Lucknow|Lucknow", "Kanpur|Kanpur", "Bahraich|Bahraich"];
    }
    for (var option in optionarray) {
        var pair = optionarray[option].split("|");
        var newOption = document.createElement("option");
        newOption.value = pair[0];
        newOption.innerHTML = pair[1];
        s2.options.add(newOption);
    }

}