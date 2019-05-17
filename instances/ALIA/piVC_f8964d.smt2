(set-info :smt-lib-version 2.6)
(set-logic ALIA)
(set-info :source |piVC|)
(set-info :category "industrial")
(set-info :status unsat)
(declare-fun V_12 () Int)
(declare-fun V_11 () Int)
(declare-fun a_0 () (Array Int Int))
(declare-fun a () (Array Int Int))
(declare-fun i () Int)
(assert (let ((?v_0 (and true (>= V_11 0))) (?v_1 (+ i 1)) (?v_2 (= V_12 V_11))) (and (and ?v_0 (and (> i 0) (and (and (<= (- 1) i) (and (< i V_12) (and (or (>= i ?v_1) (forall ((?V_21 Int)) (=> (and (<= 0 ?V_21) (<= ?V_21 i)) (forall ((?V_22 Int)) (=> (and (<= ?v_1 ?V_22) (<= ?V_22 (- V_12 1))) (<= (select a ?V_21) (select a ?V_22))))))) (and (forall ((?V_19 Int)) (=> (and (<= i ?V_19) (<= ?V_19 (- V_12 1))) (forall ((?V_20 Int)) (=> (and (<= i ?V_20) (<= ?V_20 ?V_19)) (<= (select a ?V_20) (select a ?V_19)))))) ?v_2)))) ?v_0))) (or (> 1 i) (or (>= i V_12) (or (> 0 0) (or (> 0 i) (or (and (< i ?v_1) (exists ((?V_17 Int)) (and (and (<= 0 ?V_17) (<= ?V_17 i)) (exists ((?V_18 Int)) (and (and (<= ?v_1 ?V_18) (<= ?V_18 (- V_12 1))) (> (select a ?V_17) (select a ?V_18))))))) (or (and (< (- 0 1) 0) (exists ((?V_15 Int)) (and (and (<= 0 ?V_15) (<= ?V_15 (- 0 1))) (exists ((?V_16 Int)) (and (and (<= 0 ?V_16) (<= ?V_16 0)) (> (select a ?V_15) (select a ?V_16))))))) (or (exists ((?V_13 Int)) (and (and (<= i ?V_13) (<= ?V_13 (- V_12 1))) (exists ((?V_14 Int)) (and (and (<= i ?V_14) (<= ?V_14 ?V_13)) (> (select a ?V_14) (select a ?V_13)))))) (not ?v_2)))))))))))
(check-sat)
(exit)