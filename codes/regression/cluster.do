clear
cls
display "Experiment 1"

import delimited "All_E1.csv"
quietly{
	gen tP= round_number* average_k_inpolls
	gen DP= is_treatment* average_k_inpolls
	gen DPV= is_treatment* diff_pv_lag
	gen Tdummy = 0
	replace Tdummy = 1 if round_number > 10
	gen TdummyP = Tdummy * average_k_inpolls
	gen TdummyD = Tdummy * is_treatment
	gen TdummyDP = Tdummy * is_treatment * average_k_inpolls
	gen diff_quality = 0
	replace diff_quality = 1 if quality_k_j > 20
	gen TdummyQ = Tdummy * diff_quality
	gen DQ = is_treatment* diff_quality
	gen TdummyDQ = Tdummy * is_treatment * diff_quality
}
display "E1_Model 1"
reg belief_k average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP, cluster(group)
outreg2 using E1_regression_model1.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg belief_k average_k_inpolls Tdummy TdummyP if is_treatment==1, cluster(group)
outreg2 using E1_regression_model1.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg belief_k average_k_inpolls Tdummy TdummyP if is_treatment==0, cluster(group)
outreg2 using E1_regression_model1.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E1_Model 2"
reg k_inelection average_k_inpolls is_treatment DP, cluster(group) 
outreg2 using E1_regression_model2.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls is_treatment DP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls if is_treatment==1, cluster(group)
outreg2 using E1_regression_model2.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	} 
}
reg k_inelection average_k_inpolls if is_treatment==0, cluster(group)
outreg2 using E1_regression_model2.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E1_Model 3"
reg diff_bp diff_pv_lag is_treatment DPV, cluster(group) 
outreg2 using E1_regression_model3.doc, replace ctitle(Pool)dec(3)
foreach var of varlist diff_pv_lag is_treatment DPV{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg diff_bp diff_pv_lag if is_treatment==1, cluster(group)
outreg2 using E1_regression_model3.doc, append ctitle(Treatment)dec(3)
foreach var of varlist diff_pv_lag{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg diff_bp diff_pv_lag if is_treatment==0, cluster(group)
outreg2 using E1_regression_model3.doc, append ctitle(Control)dec(3)
foreach var of varlist diff_pv_lag{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E1_Model 4"
reg k_inelection average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP, cluster(group)
outreg2 using E1_regression_model4.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls Tdummy TdummyP if is_treatment==1, cluster(group)
outreg2 using E1_regression_model4.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls Tdummy TdummyP if is_treatment==0, cluster(group)
outreg2 using E1_regression_model4.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E1_Model 5"
reg k_inelection average_k_inpolls Tdummy TdummyP diff_quality TdummyQ DP is_treatment TdummyD TdummyDP  DQ TdummyDQ, cluster(group)
outreg2 using E1_regression_model5.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP diff_quality TdummyQ TdummyDQ{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls Tdummy TdummyP diff_quality TdummyQ if is_treatment==1, cluster(group)
outreg2 using E1_regression_model5.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP diff_quality TdummyQ{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls Tdummy TdummyP diff_quality TdummyQ if is_treatment==0, cluster(group)
outreg2 using E1_regression_model5.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP diff_quality TdummyQ{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E1_Model 6"
reg belief_k average_k_inpolls Tdummy TdummyP diff_quality TdummyQ DP is_treatment TdummyD TdummyDP DQ TdummyDQ, cluster(group)
outreg2 using E1_regression_model6.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP diff_quality TdummyQ TdummyDQ{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg belief_k average_k_inpolls Tdummy TdummyP diff_quality TdummyQ if is_treatment==1, cluster(group)
outreg2 using E1_regression_model6.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP diff_quality TdummyQ{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg belief_k average_k_inpolls Tdummy TdummyP diff_quality TdummyQ if is_treatment==0, cluster(group)
outreg2 using E1_regression_model6.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP diff_quality TdummyQ{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

clear
display "Experiment 2"
import delimited "All_E2.csv"
quietly{
	gen tP= round_number* average_k_inpolls
	gen DP= is_treatment* average_k_inpolls
	gen DPV= is_treatment* diff_pv_lag
	gen Tdummy = 0
	replace Tdummy = 1 if round_number > 10
	gen TdummyP = Tdummy * average_k_inpolls
	gen TdummyD = Tdummy * is_treatment
	gen TdummyDP = Tdummy * is_treatment * average_k_inpolls
}
display "E2_Model 1"
reg belief_k average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP, cluster(group)
outreg2 using E2_regression_model1.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
} 
reg belief_k average_k_inpolls Tdummy TdummyP if is_treatment==1, cluster(group)
outreg2 using E2_regression_model1.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	} 
}
reg belief_k average_k_inpolls Tdummy TdummyP if is_treatment==0, cluster(group)
outreg2 using E2_regression_model1.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E2_Model 2"
reg k_inelection average_k_inpolls is_treatment DP, cluster(group) 
outreg2 using E2_regression_model2.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls is_treatment DP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls if is_treatment==1, cluster(group)
outreg2 using E2_regression_model2.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls if is_treatment==0, cluster(group)
outreg2 using E2_regression_model2.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E2_Model 3"
reg diff_bp diff_pv_lag is_treatment DPV, cluster(group) 
outreg2 using E2_regression_model3.doc, replace ctitle(Pool)dec(3)
foreach var of varlist diff_pv_lag is_treatment DPV{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg diff_bp diff_pv_lag if is_treatment==1, cluster(group)
outreg2 using E2_regression_model3.doc, append ctitle(Treatment)dec(3)
foreach var of varlist diff_pv_lag{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg diff_bp diff_pv_lag if is_treatment==0, cluster(group)
outreg2 using E2_regression_model3.doc, append ctitle(Control)dec(3)
foreach var of varlist diff_pv_lag{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E2_Model 4"
reg k_inelection average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP, cluster(group)
outreg2 using E2_regression_model4.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
} 
reg k_inelection average_k_inpolls Tdummy TdummyP if is_treatment==1, cluster(group)
outreg2 using E2_regression_model4.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	} 
}
reg k_inelection average_k_inpolls Tdummy TdummyP if is_treatment==0, cluster(group)
outreg2 using E2_regression_model4.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

clear
display "Experiment 3"
import delimited "All_E3.csv"
quietly{
	gen tP= round_number* average_k_inpolls
	gen DP= is_treatment* average_k_inpolls
	gen DPV= is_treatment* diff_pv_lag
	gen Tdummy = 0
	replace Tdummy = 1 if round_number > 10
	gen TdummyP = Tdummy * average_k_inpolls
	gen TdummyD = Tdummy * is_treatment
	gen TdummyDP = Tdummy * is_treatment * average_k_inpolls
}
display "E3_Model 1"
reg belief_k average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP, cluster(group)
outreg2 using E3_regression_model1.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

reg belief_k average_k_inpolls Tdummy TdummyP if is_treatment==1, cluster(group)
outreg2 using E3_regression_model1.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg belief_k average_k_inpolls Tdummy TdummyP if is_treatment==0, cluster(group)
outreg2 using E3_regression_model1.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	} 
}

display "E3_Model 2"
reg k_inelection average_k_inpolls is_treatment DP, cluster(group) 
outreg2 using E3_regression_model2.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls is_treatment DP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	} 
}
reg k_inelection average_k_inpolls if is_treatment==1, cluster(group)
outreg2 using E3_regression_model2.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls if is_treatment==0, cluster(group)
outreg2 using E3_regression_model2.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	} 
}

display "E3_Model 3"
reg diff_bp diff_pv_lag is_treatment DPV, cluster(group) 
outreg2 using E3_regression_model3.doc, replace ctitle(Pool)dec(3)
foreach var of varlist diff_pv_lag is_treatment DPV{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg diff_bp diff_pv_lag if is_treatment==1, cluster(group)
outreg2 using E3_regression_model3.doc, append ctitle(Treatment)dec(3)
foreach var of varlist diff_pv_lag{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg diff_bp diff_pv_lag if is_treatment==0, cluster(group)
outreg2 using E3_regression_model3.doc, append ctitle(Control)dec(3)
foreach var of varlist diff_pv_lag{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

display "E3_Model 4"
reg k_inelection average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP, cluster(group)
outreg2 using E3_regression_model4.doc, replace ctitle(Pool)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP DP is_treatment TdummyD TdummyDP{
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}

reg k_inelection average_k_inpolls Tdummy TdummyP if is_treatment==1, cluster(group)
outreg2 using E3_regression_model4.doc, append ctitle(Treatment)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	}
}
reg k_inelection average_k_inpolls Tdummy TdummyP if is_treatment==0, cluster(group)
outreg2 using E3_regression_model4.doc, append ctitle(Control)dec(3)
foreach var of varlist average_k_inpolls Tdummy TdummyP {
	qui boottest `var', weight(webb) nograph
	if r(p)<0.1 {
		display "_`var':" r(p)
	} 
}

