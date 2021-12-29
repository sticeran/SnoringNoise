import os
from git.repo import Repo
from git.repo.fun import is_git_dir


class GitRepositoryClass(object):
    """
    git仓库管理
    """

    def __init__(self, local_path, repo_url, branch='master'):
        self.local_path = local_path
        self.repo_url = repo_url
        self.repo = None
        self.initial(repo_url, branch)

    def initial(self, repo_url, branch):
        """
        初始化git仓库
        :param repo_url:
        :param branch:
        :return:
        """
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        git_local_path = os.path.join(self.local_path, '.git')
        if not is_git_dir(git_local_path):
            self.repo = Repo.clone_from(repo_url, to_path=self.local_path, branch=branch)
        else:
            self.repo = Repo(self.local_path)

    def pull(self):
        """
        从线上拉最新代码
        :return:
        """
        self.repo.git.pull()

    def branches(self):
        """
        获取所有分支
        :return:
        """
        branches = self.repo.remote().refs
        return [item.remote_head for item in branches if item.remote_head not in ['HEAD', ]]

    def commits(self):
        """
        获取所有提交记录
        :return:
        """
        commit_log = self.repo.git.log('--pretty={"commit":"%H","author":"%an","email":"%ae","summary":"%s","date":"%cd"}',
                                       max_count=50,
                                       date='format:%Y-%m-%d %H:%M')
        log_list = commit_log.split("\n")
        return [eval(item) for item in log_list]
    
    def git_log_command(self, command):
        """
        获取gitlog命令下的所有提交记录
        :return:
        """
        def case1():                            # 第一种情况执行的函数
            commit_log = self.repo.git.log(command[0])
            return commit_log
        def case2():                            # 第二种情况执行的函数
            commit_log = self.repo.git.log(command[0],command[1])
            return commit_log
        def case3():                            # 第三种情况执行的函数
            commit_log = self.repo.git.log(command[0],command[1],command[2])
            return commit_log
        def case4():                            # 第四种情况执行的函数
            commit_log = self.repo.git.log(command[0],command[1],command[2],command[3])
            return commit_log
        def case5():                            # 第五种情况执行的函数
            commit_log = self.repo.git.log(command[0],command[1],command[2],command[3],command[4])
            return commit_log
        def case6():                            # 第六种情况执行的函数
            commit_log = self.repo.git.log(command[0],command[1],command[2],command[3],command[4],command[5])
            return commit_log
        def case7():                            # 第七种情况执行的函数
            commit_log = self.repo.git.log(command[0],command[1],command[2],command[3],command[4],command[5],command[6])
            return commit_log
        def case8():                            # 第八种情况执行的函数
            commit_log = self.repo.git.log(command[0],command[1],command[2],command[3],command[4],command[5],command[6])
            return commit_log
        def default():                          # 默认情况下执行的函数
            return None;
            print('No such case')
        
        switch = {1: case1,                     # 注意此处不要加括号
                  2: case2,
                  3: case3,
                  4: case4,
                  5: case5,
                  6: case6,
                  7: case7,
                  8: case8,
                  }
        
        num_param = len(command)                 # 获取选择
        commit_log = switch.get(num_param, default)()         # 执行对应的函数，如果没有就执行默认的函数
        return commit_log
#         log_list = commit_log.split("\n")
#         return log_list
#         return [eval(item) for item in log_list]

    def git_show_command(self, command):
        """
        获取外部传入的带参数的git show命令下的gitshow修改信息
        :return:
        """
        def case1():                            # 第一种情况执行的函数
            commit_show = self.repo.git.show(command[0])
            return commit_show
        def case2():                            # 第二种情况执行的函数
            commit_show = self.repo.git.show(command[0],command[1])
            return commit_show
        def case3():                            # 第三种情况执行的函数
            commit_show = self.repo.git.show(command[0],command[1],command[2])
            return commit_show
        def case4():                            # 第四种情况执行的函数
            commit_show = self.repo.git.show(command[0],command[1],command[2],command[3])
            return commit_show
        def case5():                            # 第五种情况执行的函数
            commit_show = self.repo.git.show(command[0],command[1],command[2],command[3],command[4])
            return commit_show
        def case6():                            # 第六种情况执行的函数
            commit_show = self.repo.git.show(command[0],command[1],command[2],command[3],command[4],command[5])
            return commit_show
        def default():                          # 默认情况下执行的函数
            return None;
            print('No such case')
        
        switch = {1: case1,                     # 注意此处不要加括号
                  2: case2,
                  3: case3,
                  4: case4,
                  5: case5,
                  6: case6,
                  }
        
        num_param = len(command)                 # 获取选择
        commit_show = switch.get(num_param, default)()         # 执行对应的函数，如果没有就执行默认的函数
        return commit_show
#         commit_log = self.repo.git.show("%s" % commitSHA)
#         log_list = commit_log.split("\n")
#         return [eval(item) for item in log_list]

    def git_blame_command(self, command):
        """
        获取外部传入的带参数的git show命令下的gitshow修改信息
        :return:
        """
        def case1():                            # 第一种情况执行的函数
            commit_blame = self.repo.git.blame(command[0])
            return commit_blame
        def case2():                            # 第二种情况执行的函数
            commit_blame = self.repo.git.blame(command[0],command[1])
            return commit_blame
        def case3():                            # 第三种情况执行的函数
            commit_blame = self.repo.git.blame(command[0],command[1],command[2])
            return commit_blame
        def case4():                            # 第四种情况执行的函数
            commit_blame = self.repo.git.blame(command[0],command[1],command[2],command[3])
            return commit_blame
        def case5():                            # 第五种情况执行的函数
            commit_blame = self.repo.git.blame(command[0],command[1],command[2],command[3],command[4])
            return commit_blame
        def case6():                            # 第六种情况执行的函数
            commit_blame = self.repo.git.blame(command[0],command[1],command[2],command[3],command[4],command[5])
            return commit_blame
        def case7():                            # 第六种情况执行的函数
            commit_blame = self.repo.git.blame(command[0],command[1],command[2],command[3],command[4],command[5],command[6])
            return commit_blame
        def case8():                            # 第六种情况执行的函数
            commit_blame = self.repo.git.blame(command[0],command[1],command[2],command[3],command[4],command[5],command[6],command[7])
            return commit_blame
        def default():                          # 默认情况下执行的函数
            return None;
            print('No such case')
        
        switch = {1: case1,                     # 注意此处不要加括号
                  2: case2,
                  3: case3,
                  4: case4,
                  5: case5,
                  6: case6,
                  7: case7,
                  8: case8,
                  }
        
        num_param = len(command)                 # 获取选择
        commit_blame = switch.get(num_param, default)()         # 执行对应的函数，如果没有就执行默认的函数
        return commit_blame
#         commit_log = self.repo.git.show("%s" % commitSHA)
#         log_list = commit_log.split("\n")
#         return [eval(item) for item in log_list]

    def tags(self):
        """
        获取所有tag
        :return:
        """
        return [tag.name for tag in self.repo.tags]

    def change_to_branch(self, branch):
        """
        切换分值
        :param branch:
        :return:
        """
        self.repo.git.checkout(branch)

    def change_to_commit(self, branch, commit):
        """
        切换commit
        :param branch:
        :param commit:
        :return:
        """
        self.change_to_branch(branch=branch)
        self.repo.git.reset('--hard', commit)

    def reset_to_tag(self, tag):
        """
        切换版本
        :param tag:
        :return:
        """
        self.repo.git.reset('--hard', tag)

    def change_to_tag(self, tag):
        """
        切换tag
        :param tag:
        :return:
        """
        self.repo.git.checkout(tag)


    
