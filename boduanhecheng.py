import arcpy
import os

# 设置基础路径
input_base_path = "F:/tif/LAI_month"
output_base_path = "F:/tif/combine/LAI"

# 处理2001年到2024年的数据
for year in range(2001, 2025):
    print(f"\n正在处理 {year} 年数据...")
    
    # 设置输入工作空间 - 每年的LAI数据在对应的年份文件夹中
    input_workspace = os.path.join(input_base_path, str(year))
    
    # 检查输入目录是否存在
    if not os.path.exists(input_workspace):
        print(f"  {year}年: 输入目录不存在 - {input_workspace}")
        continue
        
    arcpy.env.workspace = input_workspace
    
    # 设置输出路径
    output_folder = os.path.join(output_base_path, str(year))
    output_filename = f"LAI_{year}_combine.tif"
    output_path = os.path.join(output_folder, output_filename)
    
    # 确保输出目录存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"  {year}年: 创建输出目录 - {output_folder}")
    
    # 获取所有匹配的TIFF文件 - 根据您提供的示例文件名
    pattern = f"LAI_{year}_*.tif"
    tif_files = arcpy.ListRasters(pattern)
    
    if len(tif_files) == 0:
        print(f"  {year}年: 未找到匹配的TIFF文件 (模式: {pattern})")
        continue
    
    print(f"  {year}年: 找到 {len(tif_files)} 个匹配的文件")
    
    # 显示找到的文件
    for i, file in enumerate(tif_files[:5]):  # 只显示前5个文件
        print(f"    文件 {i+1}: {file}")
    if len(tif_files) > 5:
        print(f"    ... 还有 {len(tif_files)-5} 个文件")
    
    # 按文件名排序，确保月份顺序正确
    tif_files.sort()
    
    # 使用分号分隔的字符串
    tif_list = ";".join(tif_files)
    
    try:
        # 执行波段合成
        print(f"  {year}年: 开始合成...")
        arcpy.management.CompositeBands(tif_list, output_path)
        print(f"  {year}年: 合成完成，输出文件: {output_path}")
    except Exception as e:
        print(f"  {year}年: 处理失败，错误: {str(e)}")

print(f"\n所有年份 (2001-2024) 处理完成!")