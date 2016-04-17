var express = require('express');
var router = express.Router();

var getDateString = function(date) {
    return date.getUTCFullYear() + "-" + ("0" + (date.getUTCMonth() + 1)).slice(-2) + "-" + ("0" + (date.getUTCDate())).slice(-2);
};

/* Get end date of RDSS */
router.get('/endDate', function(req, res, next) {

    var startDateString = req.query.startDate;
    var discountDays = req.query.discount;
    var startDate = (Date.parse(startDateString)) ? new Date(startDateString) : undefined; 
    var today = new Date(Date.now() + 8 * 60 * 60 * 1000);  // let today's base is the same as startDate (UTC+0) then add 8 hours, use UTC+0 as Taiwan time
    
    if (startDate) {
        // get discount days
        var discount = Number.parseInt(discountDays);
        discount = (discount) ? discount : 0;

        // calculate the end date of RDSS
        var endDate = new Date(startDate.getTime());
        endDate.setFullYear( startDate.getFullYear() + 3 );
        endDate.setDate( endDate.getDate() - discount );

        // calculate stage
        var stage = 0;  // 0: not start. 1: first stage of RDSS, 2: second stage, 3: third stage, 4: ended
        if (today >= startDate) {
            var firstStageEndDate = new Date(startDate.getTime());
            firstStageEndDate.setDate(firstStageEndDate.getDate() + 4 * 7); // 4 weeks 
            if (today < firstStageEndDate) {
                stage = 1;
            } else {
                var secondStageEndDate = new Date(startDate.getTime());
                secondStageEndDate.setFullYear(secondStageEndDate.getFullYear() + 1); // from startDate to next year,
                secondStageEndDate.setDate(secondStageEndDate.getDate() - discount);  // discount in 2nd stage
                if (today < secondStageEndDate) {
                    stage = 2;
                } else {
                    if (today < endDate) {
                        stage = 3;
                    } else {
                        stage = 4;
                    }
                }
            }
        }
        
        // calculate passed and remains days
        var remains = 0;
        var passed = 0;
        var total = 0;
        
        var base = new Date(0);
        var diff = 0;
        var diffDays = new Date(0);

        // total
        diff = endDate.getTime() - startDate.getTime();
        total = Math.ceil(diff / (24 * 60 * 60 * 1000));

        // remain
        if (stage < 4) {
            diff = endDate.getTime() - today.getTime();
            remains = Math.ceil(diff / (24 * 60 * 60 * 1000));
            diffDays.setDate(remains);
        
            // passed
            if (stage > 0) {
                diff = today.getTime() - startDate.getTime();
                passed = Math.floor(diff / (24 * 60 * 60 * 1000));
            }
        } else {
            passed = total;
        }
        
        res.send({
            "success": true,
            "startDate": getDateString(startDate),
            "discount": 30,
            "endDate":getDateString(endDate),
            "stage": stage,
            "today": getDateString(today),
            "total": total,
            "passed": passed, 
            "remain": remains,
            "formattedRemain": {
                "year":diffDays.getUTCFullYear() - base.getUTCFullYear(),
                "month":diffDays.getUTCMonth() - base.getUTCMonth(),
                "date":diffDays.getUTCDate() - base.getUTCDate()
            }
        });
    } else {
        // FIXME: error handling
        res.send({"success":false,
                  "message":"invalid start date"});
    }
});

module.exports = router;
