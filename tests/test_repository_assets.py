"""Basic repository-integrity checks; not a substitute for opening .pbix in Power BI Desktop."""
import csv
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "AdventureWorks Raw Data"
SALES_YEARS = (2020, 2021, 2022)
CSV_FILES = (
    "AdventureWorks Calendar Lookup.csv",
    "AdventureWorks Customer Lookup.csv",
    "AdventureWorks Product Categories Lookup.csv",
    "AdventureWorks Product Lookup.csv",
    "AdventureWorks Product Subcategories Lookup.csv",
    "AdventureWorks Returns Data.csv",
    "AdventureWorks Sales Data 2020.csv",
    "AdventureWorks Sales Data 2021.csv",
    "AdventureWorks Sales Data 2022.csv",
    "AdventureWorks Territory Lookup.csv",
    "Product Category Sales (Unpivot Demo).csv",
)
SCREENSHOTS = (
    "AdventureWorks-CustomerDetailDashboard.png",
    "AdventureWorks-ExecDashboard.png",
    "AdventureWorks-MapDashboard.png",
    "AdventureWorks-ProductDetailDashboard.png",
)


class RepositoryIntegrityTests(unittest.TestCase):
    def test_source_csv_files_contain_headers_and_data(self):
        for name in CSV_FILES:
            with self.subTest(csv=name):
                path = RAW / name
                self.assertTrue(path.is_file(), str(path))
                with path.open(encoding="utf-8-sig", newline="") as file:
                    reader = csv.reader(file)
                    header = next(reader, None)
                    self.assertIsNotNone(header)
                    expected_columns = 1 if name == "AdventureWorks Calendar Lookup.csv" else 2
                    self.assertGreaterEqual(len(header), expected_columns)
                    self.assertIsNotNone(next(reader, None))

    def test_sales_years_have_the_same_schema(self):
        headers = []
        for year in SALES_YEARS:
            with (RAW / f"AdventureWorks Sales Data {year}.csv").open(
                encoding="utf-8-sig", newline=""
            ) as file:
                headers.append(next(csv.reader(file)))
        self.assertEqual(headers[0], headers[1])
        self.assertEqual(headers[1], headers[2])

    def test_duplicate_sales_exports_remain_identical(self):
        for year in SALES_YEARS:
            with self.subTest(year=year):
                name = f"AdventureWorks Sales Data {year}.csv"
                canonical = (RAW / name).read_bytes()
                nested = (RAW / "Sales Data" / name).read_bytes()
                self.assertEqual(hashlib.sha256(canonical).digest(),
                                 hashlib.sha256(nested).digest())

    def test_power_bi_report_is_present(self):
        report = ROOT / "AdventureWorks Report_FINAL.pbix"
        self.assertTrue(report.is_file())
        self.assertGreater(report.stat().st_size, 1_000_000)

    def test_dashboard_screenshots_are_png_files(self):
        for name in SCREENSHOTS:
            with self.subTest(image=name):
                path = ROOT / "AdventureWorks Screenshots" / name
                self.assertTrue(path.is_file())
                with path.open("rb") as file:
                    self.assertEqual(file.read(8), b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()
