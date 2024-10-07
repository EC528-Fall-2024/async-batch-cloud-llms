# I was having errors with java paths so manually assigned here - remove/change them as needed
import os
os.environ['JAVA_HOME'] = 'C:\\Program Files\\Java\\jdk-11'
os.environ['PATH'] = os.environ['JAVA_HOME'] + '\\bin;' + os.environ['PATH']

from pyflink.datastream import StreamExecutionEnvironment,RuntimeExecutionMode

# simple script
def printer(data):
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH) # batch/streaming possible
    env.set_parallelism(1) # write all data to one file

    ds = env.from_collection(data)
    ds.print()
    env.execute()

if __name__ == '__main__':
    data = ["hello world"]
    printer(data)