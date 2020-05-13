# Django框架的初使用

***说起Django框架，肯定需要首先明确一个概念，即软件框架。下面就是第一个问题：***

##  软件框架（software framework）

### 概念界定

> 软件框架：通常指的是为了实现**某个业界标准**或完成**特定基本任务**的软件组件规范，也指为了实现**某个软件组件规范**时，提供规范所要求之**基础功能的软件产品**。[^1]

软件框架是具有基础功能的软件产品：

- 基础功能：可以理解为为了满足某类业务场景而设定的功能。
- 软件产品：软件框架是为了针对某一类软件设计问题而产生的。

### 形象理解

- 其实可以将软件框架想象成一个公司，公司中有各个职能部门，每个部门各司其职，通过部门之间的配合来完成工作，这些部门就形成了一个公司的组织架构。
- 软件框架也是如此，只是说一个公司，它是针对某一市场而成立的，而软件框架的设计是针对某一类软件问题而设计的， 其目的主要是提高软件开发效率。![在这里插入图片描述](https://img-blog.csdnimg.cn/20200119194125181.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)

> 软件框架是由各个模块组成，各个模块都会有不同特定的功能。模块与模块之间相互配合来完成软件的开发。

***在介绍完软件框架是什么之后，就需要研究一下具体的框架模式，这里介绍下MVC框架模式：***

## MVC

### 框架、设计模式、架构

笔者曾很困扰于这问题，查找了很多相关文字，作下总结和体会表述：
***基本概念：***

> **框架**通常是**代码重用**；
> **设计模式**是**设计重用**，其只有实例化之后才能用代码表示；
> **架构**则**介于两者之间**，部分代码重用，部分设计重用，有时分析也可重用。软件架构师在制作软件的时候、对软件规划的一种蓝图、一般是分层、画出各个组件的关系。[[1:1\]](https://www.cnblogs.com/Bert-Sun/p/12229836.html#fn1)

***比较：***

> - 框架与架构：架构偏于设计，框架偏于技术；
>   框架较之架构更具体更加聚焦于具体业务场景，一个架构可以通过多种框架来实现。
> - 框架与设计模式：设计模式较框架是更小的元素，更抽象；
>   一个框架中往往含有一个或多个设计模式，框架总是针对某一特定应用领域（比如说Django就是只针对web开发），但同一模式却可适用于各种应用。二者共同致力于重用，因而思想可以互相借鉴。
> - 架构与设计模式：
>   设计模式是用于解决一种特定的问题，范围较小；架构针对体系结构进行设计，范畴较大。一个架构中可能会出现多个设计模式来结果架构中的问题。

***逻辑思考顺序:***

> 在做一个项目的时候，首先设计出来的应该是架构，然后再来考虑运用什么框架和设计模式。不过平时遇到的都不是特别复杂的系统，用一些框架和设计模式足矣。[[2\]](https://www.cnblogs.com/Bert-Sun/p/12229836.html#fn2)

###  前世今生

####  前世

（1）Model（模版）-View（视图）-Controller（控制器）

> - 最初是一种软件设计模式，是为了将传统的输入（input）、处理（processing）、输出（output）任务运用到图形化用户交互模型中而设计的；
> - 随后，MVC的思想被应用在了Ｗeb开发方面，被称为Ｗeb MVC框架。

(2)
MVC的产生理念： **分工**。让专门的人去做专门的事。
MVC的核心思想： **解耦**。让不同的代码块之间降低耦合，增强代码的可扩展性和可移植性，实现向后兼容。

#### 今生

（1）web mvc框架图
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120112154169.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)
（2）具体功能介绍

- M全拼为Model： 主要封装对数据库层的访问，对数据库中的数据进行增、删、改、查操作。
- V全拼为View：用于封装结果，生成页面展示的html内容。
- C全拼为Controller：用于接收请求，处理业务逻辑，与Model和View交互，返回结果。

***介绍完相关基础概念后，下面对就Django框架进行整体逻辑和具体流程的了解：***

##  Django整体逻辑

###  简介

> - 主要目的是**简便、快速**的开发**数据库驱动**的网站
> - 强调**代码复用**，多个组件可以很方便的以"插件"形式服务于整个框架，Django有许多功能强大的第三方插件，你甚至可以很方便的开发出自己的工具包。
> - 具有很强的**可扩展性**。

Django框架**遵循MVC**设计，并且有一个专有名词：**MVT**

###  MVT

（1）Django MVT框架图
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120133518974.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)
（2）具体功能介绍：

- **M（Model层）**：与MVC中的M功能相同，负责和数据库交互，进行数据处理。
  - (课上说的持久化层也是在这里)
- **V（View层，业务逻辑层）**：接收请求，进行业务处理，返回应答。
- **url.py（Controller，控制器层）**，与MVC中的C功能相同，负责接受用户请求并分发对应的视图。
  - 当然这个url层是我自己定义的，我认为url.py充当的是一个路由的角色，书本上对于控制器层的标准定义是：主要用于接受界面层提交的请求并管理和分析这些请求业务的类型，进而转发给业务逻辑层的业务对象。
- **T（Template，用户界面GUI层）**：与MVC中的V功能相同，负责封装构造要返回的html。



> 也就是说，

##  Django项目的构建流程

###  搭建环境

***问1:***
如果在一台机器上，想开发多个不同的项目，需要用到同一个包的不同版本，如果还使用`sudo pip3 install 包名称`的命令，在同一个目录下安装或者更新，其它的项目必须就无法运行了，怎么办呢？

> 答1:使用**虚拟环境**。

***问2：***
什么是虚拟环境？

> 答2:虚拟环境其实就**是对真实pyhton环境的复制**。
> 这样我们在复制的python环境中再去安装相应的包就不会影响到真实的python环境了。
> 通过建立多个虚拟环境，在不同的虚拟环境中开发项目就实现了项目之间的隔离。

####  虚拟环境安装

（1）首先安装虚拟环境，命令如下:

```powershell
sudo pip3 install virtualenv #安装虚拟环境
```

（2）接下来还要安装虚拟环境扩展包，命令如下：

```powershell
sudo pip3 install virtualenvwrapper #安装虚拟环境包装器的目的是使用更加简单的命令来管理虚拟环境。
```

（3）修改用户家目录下的隐藏配置文件`.bashrc`,在文件最后处添加如下内容：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120145611529.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)

```powershell
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
```

（4）创建python3虚拟环境的命令如下：

```powershell
mkvirtualenv -p python3 虚拟环境名称
例：
mkvirtualenv -p python3 test1_py3
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120151034547.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)
***综述：***

> 创建成功后，会自动工作在这个虚拟环境上。
> 创建虚拟环境需要联网。
> 工作在虚拟环境上，提示符最前面会出现"(虚拟环境名称)"。
> 所有的虚拟环境，都位于/home/您的用户名/下的隐藏目录.virtualenvs下。

####  虚拟环境相关终端语句操作

- 退出虚拟环境：`deactivate`

- 查看所有虚拟环境：`workon 两次tab键`

- 使用虚拟环境：`workon 虚拟环境名称`

- 删除虚拟环境：`rmvirtualenv 虚拟环境名称`

  > 例： 先退出：`deactivate`；再删除：`rmvirtualenv py_django`

- 在虚拟环境中可以使用pip命令操作python包：`pip install 包名称`

  > 注意：在虚拟环境中不可使用`sudo pip install 包名称` 来安装`python包`，这样安装的包实际是安装在了真实的主机环境上。

- 查看已安装的python包：`pip list` or `pip freeze`

  > 这两个命令都可以查看当前工作的虚拟环境中安装了哪些python包，只是显示的格式稍有不同。

- 安装django包：`pip install django==1.8.2`

  > 如果前面删除过虚拟环境py_django，则需要先创建一下，否则直接安装django包即可。![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120152944776.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)

####  自我总结

- 在为了避免在正式环境下创建多个项目而导致相关安装包的冲突，从而进行虚拟环境安装后，我们就可以在我们安装的的虚拟环境中进行Django项目的创建了。
- 逻辑关系上是我们可以根据我们的需求创建多个虚拟环境，而在每个虚拟环境下我们就可以进行相关Django项目的创建

> 在不同的虚拟环境下我们可以自由的根据该虚拟环境下Django项目的需要进行相关包的安装，这样就解决了前文所说的同一个包不同版本之间的替代问题。

***下面就介绍下Django项目的创建：***

###  创建Django项目

**强调一下，创建Django项目前：**

> 一是要在正确的虚拟环境中间（即要进入4.1步骤中已经创建好的虚拟环境中）；
> 二是方便后期相关文件管理，我们最好创建该项目的专属文件夹。
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200121123035877.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)

####  创建Django的命令

创建项目的命令如下：

```powershell
django-admin startproject 项目名称
例：
django-admin startproject test1
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200121123822654.png)

####  Django项目默认目录说明

进入4.2.1创建的Django项目test1目录，查看目录树形结构
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200121124917186.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)

- `manage.py`是项目管理文件，通过它管理项目。
- 与项目同名的目录，此处为`test1`。
- `_init_.py`是一个空文件，作用是这个目录test1可以被当作包使用。
- `settings.py`是项目的整体配置文件。
- `urls.py`是项目的URL配置文件。
- `wsgi.py`是项目与WSGI兼容的Web服务器入口。

***在django中，项目的组织结构为一个项目包含多个应用，一个应用对应一个业务模块。下面对应用进行介绍：***

###  创建Django项目下的应用

Django中对于应用的操作分为***创建***和***安装***，下面分别介绍：

####  应用的创建

创建应用的命令如下：

```powershell
python manage.py startapp 应用名
例如：
python manage.py startapp test_app
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200122205712683.png)
应用默认目录说明：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200122211351633.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)

- `_init.py_`是一个空文件，表示当前目录booktest可以当作一个python包使用。
- `tests.py`文件用于开发测试用例，在实际开发中会有专门的测试人员，这个事情不需要我们来做。
- `models.py`文件跟数据库操作相关。
- `views.py`文件跟接收浏览器请求，进行处理，与M和T进行交互，返回页面，定义处理视图函数。
- `admin.py`文件跟网站的后台管理相关。
- `migrations`文件夹之后给大家介绍。

***应用创建成功后，需要安装才可以使用，也就是建立应用和项目之间的关联；***

####  应用的安装

建立应用和项目之间的联系，需要对应用进行注册。
修改`settings.py`中的`INSTALLED_APPS`配置项。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200122213917882.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200122215243957.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)

###  运行服务器

通过上面的一些了操作，就可以使用django提供的一个纯python编写的轻量级web服务器，仅在开发阶段使用。
运行服务器命令如下：

```powershell
python manage.py runserver ip:端口
例：
python manage.py runserver
```

> 可以不写IP和端口，默认IP是127.0.0.1，默认端口为8000。
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200122220247908.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200122220636590.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTIyOTk4Mg==,size_16,color_FFFFFF,t_70)

------

[^1]:百度百科-软件框架 [link](https://baike.baidu.com/item/软件框架/1471931?fr=aladdin)
[^2]:架构、框架和设计模式 [link](https://blog.csdn.net/honeyht/article/details/80596881)

