"""Rebrand contract for the seller app: bitposta.com replaces every old domain.

Backward compatibility is deliberately not required for the site/reference
strings. The TAG URL is different: tags already written and locked carry the
old address, so its change is gated on an explicit owner decision.
"""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORE = ROOT / "core/src/main/java/com/saebm/btcnfcseller/core"

BRAND = "bitposta.com"
LEGACY = ("btc4.fun", "b.tc4fun.ir", "bitcoin4.fun", "btc4-fun")


class SellerRebrand(unittest.TestCase):
    def test_address_transport_uses_the_new_host(self):
        source = (CORE / "AddressTransport.java").read_text()
        self.assertIn(f'"{BRAND}", 443', source)
        for legacy in LEGACY:
            with self.subTest(legacy=legacy):
                self.assertNotIn(legacy, source)

    def test_tag_provisioning_validates_the_new_tag_url(self):
        source = (CORE / "TagProvisioning.java").read_text()
        self.assertIn(f'"https://{BRAND}/s/" + returnedSerial', source)
        for legacy in LEGACY:
            with self.subTest(legacy=legacy):
                self.assertNotIn(legacy, source)

    def test_no_legacy_domain_survives_in_main_sources(self):
        for path in CORE.glob("*.java"):
            with self.subTest(path=path.name):
                text = path.read_text()
                for legacy in LEGACY:
                    self.assertNotIn(legacy, text)

    def test_application_id_is_unchanged_so_installs_upgrade(self):
        gradle = (ROOT / "app/build.gradle").read_text()
        self.assertIn("com.saebm.btcnfcseller", gradle)


if __name__ == "__main__":
    unittest.main()
