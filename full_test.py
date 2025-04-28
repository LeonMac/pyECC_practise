import itertools
import os
import subprocess
import tempfile

# 定义各配置项的取值

config_options = {
    'USE_JCB': [True, False],
    'TIMING_MEASURE': [True, False],
    'ADD_FMT': ['dec', 'hex']  
}

# 生成所有组合, total 2x2x2=8 种
keys = list(config_options.keys())
value_combinations = itertools.product(*config_options.values())

for combo in value_combinations:
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 生成config.py内容
        config_content = f""" # Auto-generated config
                                USE_JCB = {combo[0]}
                                TIMING_MEASURE = {combo[1]}
                                ADD_FMT = '{combo[2]}'
                                """
        # 写入临时文件
        config_path = os.path.join(temp_dir, 'config.py')
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        # 设置环境变量，优先从临时目录导入配置
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{temp_dir}{os.pathsep}{env.get('PYTHONPATH', '')}"
        
        # 运行测试并捕获输出
        print(f"\n测试配置: {keys} = {combo}")
        result = subprocess.run(
            ['python', 'pyECC.py'],  # 确保路径正确
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT  # 合并错误输出
        )
        
        # 输出结果
        if result.returncode == 0:
            print("结果: 成功")
        else:
            print("结果: 失败")
            print("输出信息:\n", result.stdout)

'''
动态生成配置：通过itertools.product生成所有可能的配置组合。

隔离测试环境：使用临时目录为每个组合生成独立的config.py，避免修改原文件。

控制模块导入：通过设置PYTHONPATH环境变量，使Python优先从临时目录加载配置。

自动清理：tempfile.TemporaryDirectory会在测试完成后自动删除临时文件。

注意事项
路径问题：确保pyECC.py的路径正确，或在subprocess.run中指定绝对路径。

错误处理：根据需要调整结果处理逻辑（如记录日志、失败重试等）。

并行化：如需加速测试，可使用多进程（但需确保临时目录隔离）。


'''

''' 结果：

$ python full_test.py 

测试配置: ['USE_JCB', 'TIMING_MEASURE', 'ADD_FMT'] = (True, True, 'dec')
结果: 成功

测试配置: ['USE_JCB', 'TIMING_MEASURE', 'ADD_FMT'] = (True, True, 'hex')
结果: 成功

测试配置: ['USE_JCB', 'TIMING_MEASURE', 'ADD_FMT'] = (True, False, 'dec')
结果: 成功

测试配置: ['USE_JCB', 'TIMING_MEASURE', 'ADD_FMT'] = (True, False, 'hex')
结果: 成功

测试配置: ['USE_JCB', 'TIMING_MEASURE', 'ADD_FMT'] = (False, True, 'dec')
结果: 成功

测试配置: ['USE_JCB', 'TIMING_MEASURE', 'ADD_FMT'] = (False, True, 'hex')
结果: 成功

测试配置: ['USE_JCB', 'TIMING_MEASURE', 'ADD_FMT'] = (False, False, 'dec')
结果: 成功

测试配置: ['USE_JCB', 'TIMING_MEASURE', 'ADD_FMT'] = (False, False, 'hex')
结果: 成功


'''