# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.util as util
import benchexec.tools.template
import benchexec.result as result


class Tool(benchexec.tools.template.BaseTool):
    """
    Wrapper for 2LS (http://www.cprover.org/2LS).
    """

    REQUIRED_PATHS = ["2ls", "2ls-binary", "goto-cc"]

    def executable(self):
        return util.find_executable("2ls")

    def name(self):
        return "2LS"

    def version(self, executable):
        return self._version_from_tool(executable)

    def cmdline(self, executable, options, tasks, propertyfile, rlimits):
        if propertyfile:
            options = options + ["--propertyfile", propertyfile]

        return [executable] + options + tasks

    def determine_result(self, returncode, returnsignal, output, isTimeout):
        if ((returnsignal == 9) or (returnsignal == 15)) and isTimeout:
            status = "TIMEOUT"
        elif returnsignal == 9:
            status = "OUT OF MEMORY"
        elif returnsignal != 0:
            status = "ERROR(SIGNAL " + str(returnsignal) + ")"
        elif returncode == 0:
            status = result.RESULT_TRUE_PROP
        elif returncode == 10:
            if len(output) > 0:
                result_str = output[-1].strip()
                if result_str == "FALSE(valid-memtrack)":
                    status = result.RESULT_FALSE_MEMTRACK
                elif result_str == "FALSE(valid-deref)":
                    status = result.RESULT_FALSE_DEREF
                elif result_str == "FALSE(valid-free)":
                    status = result.RESULT_FALSE_FREE
                elif result_str == "FALSE(no-overflow)":
                    status = result.RESULT_FALSE_OVERFLOW
                elif result_str == "FALSE(termination)":
                    status = result.RESULT_FALSE_TERMINATION
                elif result_str == "FALSE(valid-memcleanup)":
                    status = result.RESULT_FALSE_MEMCLEANUP
                else:
                    status = result.RESULT_FALSE_REACH
            else:
                status = result.RESULT_FALSE_REACH
        else:
            status = result.RESULT_UNKNOWN
        return status
