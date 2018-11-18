import unittest

from patcher import get_patch_ver, get_patches, get_rollbacks, sort_patches, apply_patches


class PatcherTest(unittest.TestCase):
    def test_get_patch_ver(self):
        data = "/dir/patches/1.sql"
        output = get_patch_ver(data)
        expected = 1
        self.assertEqual(expected, output)

        data = "/dir/patches/2_vfd.sql"
        output = get_patch_ver(data)
        expected = 2
        self.assertEqual(expected, output)

    def test_get_patches(self):
        data = ["/dir/patches/1.sql", "/dir/patches/3.sql", "/dir/patches/1_rollback.sql"]
        output = get_patches(data)
        expected = ["/dir/patches/1.sql", "/dir/patches/3.sql"]
        self.assertEqual(expected, output)

    def test_get_rollbacks(self):
        data = ["/dir/patches/1.sql", "/dir/patches/3.sql", "/dir/patches/1_rollback.sql"]
        output = get_rollbacks(data)
        expected = ["/dir/patches/1_rollback.sql"]
        self.assertEqual(expected, output)

    def test_sort_patches(self):
        data = ["/dir/patches/3.sql", "/dir/patches/10_something.sql", "/dir/patches/2_roll.sql"]
        output = sort_patches(data)
        expected = ["/dir/patches/2_roll.sql", "/dir/patches/3.sql", "/dir/patches/10_something.sql"]
        self.assertEqual(expected, output)

    def test_sort_patches_reverse(self):
        data = ["/dir/patches/3.sql", "/dir/patches/10_something.sql", "/dir/patches/2_roll.sql"]
        output = sort_patches(data, reverse=True)
        expected = ["/dir/patches/10_something.sql", "/dir/patches/3.sql", "/dir/patches/2_roll.sql", ]
        self.assertEqual(expected, output)

    def test_apply_patches(self):
        data = ["/dir/patches/1.sql", "/dir/patches/2.sql", "/dir/patches/3.sql"]
        output = apply_patches(data)
        expected = 3  # last correct patch version
        self.assertEqual(expected, output)


    def test_apply_rollback_patches(self):
        data = ["/dir/patches/1.sql", "/dir/patches/2.sql", "/dir/patches/3.sql"]
        output = apply_patches(data, rollback=True)
        expected = 1  # last correct patch version
        self.assertEqual(expected, output)

if __name__ == '__main__':
    unittest.main()
