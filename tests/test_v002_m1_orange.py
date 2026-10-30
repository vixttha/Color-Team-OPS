"""Orange: cross-mission and cross-revision negative regression scenarios.

Uses synthetic fixtures; never certifies identity or producer authenticity.
"""
import unittest
from test_v002_m1_bridge import scenario
from policy_v002.m1_bridge import reconcile_reference


class OrangeCrossScopeTests(unittest.TestCase):
    def check(self, edit, code):
        data=scenario()
        edit(data)
        verdict=reconcile_reference(**data)
        self.assertEqual((verdict.status,verdict.code),("BLOCKED",code))

    def test_foreign_work_mission(self):
        self.check(lambda d:d["work_orders"][0].update(mission_id="foreign"),"TASK_PROVENANCE_MISMATCH")
    def test_stale_work_source(self):
        self.check(lambda d:d["work_orders"][0].update(source_sha="b"*40),"TASK_PROVENANCE_MISMATCH")
    def test_foreign_worker_mission(self):
        self.check(lambda d:d["worker_events"][0].update(mission_id="foreign"),"TASK_PROVENANCE_MISMATCH")
    def test_stale_worker_source(self):
        self.check(lambda d:d["worker_events"][0].update(source_sha="b"*40),"TASK_PROVENANCE_MISMATCH")
    def test_foreign_aggregate_gate(self):
        self.check(lambda d:d["gate_records"][0].update(mission_id="foreign"),"AGGREGATE_GATE_INVALID")
    def test_foreign_transition_mission(self):
        self.check(lambda d:d["transition_events"][1].update(mission_id="foreign"),"TRANSITION_LINK_MISMATCH")
    def test_stale_transition_source(self):
        self.check(lambda d:d["transition_events"][2].update(source_sha="b"*40),"TRANSITION_LINK_MISMATCH")
    def test_foreign_head_decision_mission(self):
        self.check(lambda d:d["head_decision"].update(mission_id="foreign"),"HEAD_DECISION_MISMATCH")
    def test_foreign_order_authorization_ref(self):
        self.check(lambda d:d["work_orders"][0].update(authorization_ref="foreign"),"TASK_PROVENANCE_MISMATCH")
