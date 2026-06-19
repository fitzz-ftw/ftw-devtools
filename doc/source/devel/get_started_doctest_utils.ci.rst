Get started with Doctests Utils
==================================


>>> from fitzzftw.devtools.doctest_utils import dtprint

>>> dtprint("Only shown in terminal.")


>>> from fitzzftw.devtools.doctest_utils import NotVerbosePrint

>>> nvp = NotVerbosePrint(verbose=False)

>>> nvp("Printed to Terminal only")

>>> vp = NotVerbosePrint(verbose=True)

>>> vp("Not printet at all.")

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment

>>> env = TestHomeEnvironment("doc/source/devel/testhome",
...         appname="ftw", appauthor= "FitzzTeXnikWelt" )

>>> from fitzzftw.devtools.doctest_utils import TestArtifactCollector

>>> testdata_collector = TestArtifactCollector("doc/source/devel/testdata")




>>> env.setup()



>>> test_file_path = env.copy2cwd("testcopy.txt")



>>> testdata_noclean =  TestArtifactCollector("doc/source/devel/testdata", 
...                                            clean_dir=False)

>>> del testdata_noclean

>>> testdata_collector.base_dir.as_posix() # doctest: +ELLIPSIS
'...devel/testdata'


>>> test_saved_path = testdata_collector.export("testcopy.txt", "test")

>>> test_saved_path.exists()
True

>>> testdata_collector._clean_dir()

>>> test_saved_path.exists()
False

>>> testdata_collector("testcopy.txt", "test")

>>> test_saved_path.exists()
True



>>> testdata_collector._clean_dir()

>>> testdata_collector.base_dir.rmdir()

>>> env.clean_output()

>>> env.clean_home()

>>> env.teardown()
