% runTests.m
import matlab.unittest.TestSuite
import matlab.unittest.TestRunner
import matlab.unittest.plugins.TAPPlugin
import matlab.unittest.plugins.ToFile

suite = TestSuite.fromClass(?SampleTests);
runner = TestRunner.withTextOutput('Verbosity', 3);

% Create a TAP plugin for continuous integration systems
tapFile = 'results.tap';
plugin = TAPPlugin.producingOriginalFormat(ToFile(tapFile));

% Add the plugin to the test runner
runner.addPlugin(plugin);

% Run the tests
results = runner.run(suite);

% Exit MATLAB with a non-zero status if any tests fail
if any([results.Failed])
    exit(1);
else
    exit(0);
end