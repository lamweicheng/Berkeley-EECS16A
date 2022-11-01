q_ans = {"C_E1_F" : 88.539999e-12,
        "C_F_E2" : 88.539999e-12,
        "C_Delta" : 4.42699995e-11,
        "v_w_touch" : 0.5646713084365674,
        "v_ref" : 0.5111247668815468}
    
q_exp = {"C_E1_F" : "Plugging in the values for dimensions (d and A) as well as the given epsilon and kappa (k) values into the equation for capacitance should yield the correct answer.",
         "C_F_E2" : "Plugging in the values for dimensions (d and A) as well as the given epsilon and kappa (k) values into the equation for capacitance should yield the correct answer.",
        "C_Delta" : "Applying the formula for equivalent series capacitance should yield the correct answer. When we're dealing with just 2 capacitors, this is basically applying the *parallel* operator. In this case, C_E1_F = C_F_E2. Therefore, C_Delta = C_E1_F // C_F_E2 = C_E1_F * C_F_E2 / (C_E1_F + C_F_E2) = C_E1_F/2.",
        "v_no_touch" : "Recall that charge is conserved in \"floating\" nodes. V+ is floating since it is connected to only capacitor plates in Phase 4. Thus, the charge on those plates must be conserved. In Phase 3, the charge on C_ref = 0, since C_ref was just grounded. However, the charge on C_pixel = Vdd * C_pixel. Thus, in Phase 4, the combined charge on C_ref and C_pixel is Vdd * C_pixel, which yields the following equivalence: V+ * C_pixel + V+ * C_ref = Vdd * C_pixel. We can solve for V+ using C_pixel = C_pixel_no_touch.",
        "v_w_touch": "Recall that charge is conserved in \"floating\" nodes. V+ is floating since it is connected to only capacitor plates in Phase 4. Thus, the charge on those plates must be conserved. In Phase 3, the charge on C_ref = 0, since C_ref was just grounded. However, the charge on C_pixel = Vdd * C_pixel. Thus, in Phase 4, the combined charge on C_ref and C_pixel is Vdd * C_pixel, which yields the following equivalence: V+ * C_pixel + V+ * C_ref = Vdd * C_pixel. We can solve for V+ using C_pixel = C_pixel_w_touch.",
        "v_ref" : "We can select a good v_ref value by choosing something in between v_no_touch and v_w_touch. To best protect us from noise, a good option would be to choose the arithmetic mean of v_no_touch and v_w_touch, i.e., (v_no_touch + v_w_touch)/2."}

def autograde(answer=-1, question="3a-1", no_check=False, no_exp_if_cor=False, tolerance_pct=5.0):
    answer = float(answer)
    correct = True
    if no_check:
        pass
    elif q_ans[question] == 0 and answer == 0:
        print("Correct!")
    elif (q_ans[question] != 0) and (abs(q_ans[question]-answer))*100.0/q_ans[question] <= tolerance_pct:
        print("Correct!")
    else:
        print("Sorry, that's not quite right.")
        correct = False
    if no_exp_if_cor and correct:
        pass
    else:
        print(q_exp[question])