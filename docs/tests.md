# Tests

In this space you can find more information on the testing infrastructure for the vAccel stack. We provide information on the test framework we use, as well as examples on how to develop a test. Finally, we include tests coverage information.

#### Testing framework

We use Catch2 for our testing framework. Catch2 is very simple to include in our tests. With the use of a single header file - we just drag and drop the header in our testing directory.

#### Example test

An example of a basic test here:

```
#include <catch.hpp>
#include <utils.hpp>

extern "C" {
#include <dlfcn.h>
#include <stdbool.h>
#include <string.h>
#include <vaccel.h>
}


TEST_CASE("plugin_register") {

    int ret;
    struct vaccel_plugin plugin;
    struct vaccel_plugin_info pinfo;
    plugin.info = &pinfo;
    plugin.info->name = pname;
    list_init_entry(&plugin.entry);
    list_init_entry(&plugin.ops);
    plugin.info->init = init;
    plugin.info->fini = fini;

    ret = plugins_bootstrap();
    REQUIRE(ret == VACCEL_OK);

    ret = register_plugin(&plugin);
    REQUIRE(ret == VACCEL_OK);

    ret = plugins_shutdown();
    REQUIRE(ret == VACCEL_OK);
}
```

Catch2 has two assertions we can use, ```REQUIRE``` like the ones above, and ```CHECK``` where the test will not terminate even if it fails.

Instead of traditional fixtures, we use ```SECTIONS``` to set up and tear down our tests easily. The main benefit of this is that it is more readable this way compared to traditional tests:

```
TEST_CASE("plugin_register") {

    struct vaccel_plugin plugin;
    struct vaccel_plugin_info pinfo;
    plugin.info = &pinfo;
    plugin.info->name = pname;
    list_init_entry(&plugin.entry);
    list_init_entry(&plugin.ops);
    plugin.info->init = init;
    plugin.info->fini = fini;

    plugins_bootstrap();

    SECTION("normal plugin initialisation") 
    {
        REQUIRE(register_plugin(&plugin) == VACCEL_OK);
        REQUIRE(unregister_plugin(&plugin) == VACCEL_OK);
    }

    SECTION("null plugin initialisation")
    {
        REQUIRE(register_plugin(NULL) == VACCEL_EINVAL);
    }

    plugins_shutdown();
}
```

#### Adding tests to the main test runner

Very simple within the ```CMakeLists.txt``` in the test directory. 

Add your test name to one of the sets ```CORE``` or ```API``` 

```
set(TESTS_CORE
    test_example
    .
    .
    test_name
)
```

And then add the test name to one of the ```set_tests_properties()``` to set the properties you require for tests in the same file.


#### Running tests

To run tests locally:

```cmake ../ -DBUILD_PLUGIN_NOOP=ON -DENABLE_TESTS=ON```

and then 

```make && make test```

Our current test coverage can be seen here: 

[Tests coverage](/coverage/coverage.md)

And for more information regarding the testing framework have a look at ```docs/coverage``` folder.
