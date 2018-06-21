# nlpcc_slu

##关于这个代码

这个代码是基于nlpcc比赛的数据music所做的一个领域分类与意图识别任务。

constant.py：代码中经常用到的一个常量, 比如间隔符号等等。
corpus_parser.py：对corpus目录下的标注语料的解析器, 由于后续可能会添加不同领域的标注语料, 语料的标注格式不尽相同, 所以对应的标注语料有相应的语料解析器是合理的。
feature.py：主要是一些特征类。
model.py：模型类。
session.py：主要是对语料一个对话片段的封装。
utils.py：常用到的一些api, 比如文件处理等。
