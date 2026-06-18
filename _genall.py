# -*- coding: utf-8 -*-
"""批次產生 A/B/C 三卷每個編號大題的幾何圖。"""
from _figgen import (quad, triangle, parallel_lines, sticks, objects,
                     shapes_chart, two_transversals, RED, EDGE, GREEN, PURPLE)

R, B = '#c0392b', '#2e6da4'

# ===================== A 卷（星星）=====================
# 第三關 平行四邊形
quad('fA3q2.png', 'para', side_labels={'AD': '8', 'AB': '5'},
     caption='平行四邊形 ABCD（AD=8、AB=5）')
quad('fA3q3.png', 'para', angle_at={'A': '70°'},
     caption='平行四邊形 ABCD（∠A=70°）')
# 第五關 生活幾何
objects('fA5q1.png',
        [('教室的門', 'rect'), ('撲克牌方塊', 'rhombus'),
         ('風箏', 'kite'), ('棋盤格', 'square'),
         ('梯形口袋', 'trap')],
        caption='想一想：這些生活物品，像哪一種四邊形？')

# ===================== B 卷（月亮）=====================
# 第一大題 三角形
sticks('fB1q1.png',
       [('(a) 5,7,10', [5, 7, 10]), ('(b) 3,4,8', [3, 4, 8]),
        ('(c) 6,6,11', [6, 6, 11])],
       caption='兩短邊相加 > 最長邊 才能組成三角形')
triangle('fB1q2.png', sides={'BC': '8', 'AB': '5', 'CA': 'x'},
         lengths=(8, 6, 5), caption='已知兩邊 5、8，求第三邊 x')
triangle('fB1q3.png', sides={'BC': '9', 'AB': '4', 'CA': 'x'},
         lengths=(9, 7, 4), caption='已知兩邊 4、9，求第三邊 x')
triangle('fB1q4.png', sides={'AB': '500', 'BC': '300', 'CA': 'x'},
         lengths=(300, 400, 500),
         caption='家→學校 直走 500 ／ 轉彎走 300 再走 x')
# 第二大題 平行線（Q1 已有圖）
parallel_lines('fB2q2.png',
               marked=[('br1', '∠1=110°', R), ('tr2', '∠2=?', B)],
               caption='同側內角（在兩線之間、截線同一邊）')
parallel_lines('fB2q3.png',
               marked=[('br1', '∠1=75°', R), ('tl2', '∠2=?', B)],
               caption='內錯角（在兩線之間、截線兩邊交錯）')
parallel_lines('fB2q4.png', show_numbers=True,
               caption='8 個角：同位角、內錯角、同側內角')
parallel_lines('fB2q5.png', l1='甲', l2='乙', tname='丙', note='甲 // 乙',
               marked=[('br1', '80°', R), ('tr2', '?', B)],
               caption='兩平行步道甲乙，被斜路丙穿過')
# 第三大題 平行四邊形
quad('fB3q1.png', 'para', side_labels={'AD': '12', 'AB': '7'},
     caption='平行四邊形 ABCD（AD=12、AB=7）')
quad('fB3q2.png', 'para', angle_at={'A': '55°'},
     caption='平行四邊形 ABCD（∠A=55°）')
quad('fB3q3.png', 'para', diagonals=True, O_label=True,
     diag_labels={'AO': '6', 'BO': '4'},
     caption='對角線交於 O（AO=6、BO=4）')
quad('fB3q4.png', 'para', diagonals=True, O_label=True,
     ticks=[('AD', 1, GREEN), ('BC', 1, GREEN), ('AB', 2, PURPLE),
            ('DC', 2, PURPLE)],
     caption='平行四邊形的判別性質')
quad('fB3q5.png', 'para', side_labels={'AD': '120', 'AB': '80'},
     angle_at={'A': '70°'}, caption='飛毯座椅框架（平行四邊形）')
# 第四大題 特殊四邊形
shapes_chart('fB4q1.png', caption='特殊四邊形家族參考圖')
quad('fB4q2.png', 'rhombus',
     ticks=[('AB', 1, GREEN), ('BC', 1, GREEN), ('CD', 1, GREEN),
            ('DA', 1, GREEN)],
     caption='菱形（四邊等長），周長 36')
quad('fB4q3.png', 'rect', diagonals=True, O_label=True,
     right_angles=['A', 'B', 'C', 'D'], diag_labels={'AC': '10'},
     caption='長方形（對角線等長），AC=10')
quad('fB4q4.png', 'kite',
     side_labels={'AB': '6', 'DA': '6', 'BC': '12', 'CD': '12'},
     ticks=[('AB', 1, GREEN), ('DA', 1, GREEN), ('BC', 2, PURPLE),
            ('CD', 2, PURPLE)],
     caption='箏形（兩組鄰邊等長）')
quad('fB4q5.png', 'trap', angle_at={'A': '65°'},
     ticks=[('BC', 1, GREEN), ('DA', 1, GREEN)],
     caption='等腰梯形 ABCD（AB // CD）')
quad('fB4q6.png', 'rhombus', diagonals=True, O_label=True,
     diag_labels={'AC': '8', 'BD': '6'},
     caption='菱形，對角線 AC=8、BD=6')

# ===================== C 卷（太陽）=====================
# 第一大題 選擇
sticks('fC1q1.png',
       [('(A) 2,3,6', [2, 3, 6]), ('(B) 1,1,3', [1, 1, 3]),
        ('(C) 5,7,11', [5, 7, 11]), ('(D) 4,5,10', [4, 5, 10])],
       caption='哪一組可以組成三角形？')
parallel_lines('fC1q2.png',
               marked=[('br1', '72°', R), ('tr2', '?', B)],
               caption='截線與 L₁ 夾角 72°，求同側內角')
quad('fC1q3.png', 'para', angle_at={'A': '∠A', 'B': '∠B'},
     caption='平行四邊形（∠A = 3∠B）')
quad('fC1q4.png', 'para', diagonals=True, O_label=True,
     ticks=[('AD', 1, GREEN), ('BC', 1, GREEN)],
     caption='平行四邊形的性質')
quad('fC1q5.png', 'square', diagonals=True, O_label=True,
     right_angles=['A', 'B', 'C', 'D'],
     ticks=[('AB', 1, GREEN), ('BC', 1, GREEN), ('CD', 1, GREEN),
            ('DA', 1, GREEN)],
     caption='正方形的兩條對角線')
# 第二大題 填充
triangle('fC2q1.png', sides={'BC': '12', 'AB': '7', 'CA': 'x'},
         lengths=(12, 9, 7), caption='兩邊 7、12，求第三邊 x 範圍')
triangle('fC2q2.png', sides={'BC': '10', 'AB': '6', 'CA': 'x'},
         lengths=(10, 8, 6), caption='兩邊 6、10，第三邊為偶數')
parallel_lines('fC2q3.png', marked=[('br1', '∠1=48°', R)],
               caption='求 ∠1 的內錯角、同側內角')
quad('fC2q4.png', 'para', side_labels={'AB': '15', 'BC': '9'},
     caption='平行四邊形（AB=15、BC=9）')
quad('fC2q5.png', 'para', diagonals=True, O_label=True,
     diag_labels={'AC': '16', 'BD': '10'},
     caption='平行四邊形對角線（AC=16、BD=10）')
quad('fC2q6.png', 'rhombus', diagonals=True, O_label=True,
     diag_labels={'AC': '10', 'BD': '24'},
     caption='菱形對角線 AC=10、BD=24')
quad('fC2q7.png', 'trap', angle_at={'A': '72°'},
     ticks=[('BC', 1, GREEN), ('DA', 1, GREEN)],
     caption='等腰梯形（AB // CD，∠A=72°）')
quad('fC2q8.png', 'square', diagonals=True, O_label=True,
     right_angles=['A', 'B', 'C', 'D'], diag_labels={'AC': '10'},
     caption='正方形，對角線長 10')
# 第三大題 計算
triangle('fC3q1.png', sides={'AB': 'x+3', 'BC': '2x-1', 'CA': 'x+7'},
         caption='三角形三邊為代數式')
two_transversals('fC3q2.png', a1='100°', a2='127°',
                 caption='兩截線 M1、M2，求 ∠3、∠4')
quad('fC3q3.png', 'para', angle_at={'A': '∠A', 'B': '∠B'},
     caption='平行四邊形（∠A 比 ∠B 多 40°）')
quad('fC3q4.png', 'rect', diagonals=True, O_label=True,
     right_angles=['A', 'B', 'C', 'D'], side_labels={'AB': '6'},
     diag_labels={'AO': '5'}, caption='長方形（OA=5、AB=6，求 AD）')
# 第四大題 素養
triangle('fC4q1.png', sides={'AB': '40', 'CA': '60', 'BC': 'x'},
         lengths=(50, 60, 40), caption='三根竹子 40、60、x 做三角形框架')
parallel_lines('fC4q2.png', l1='上步道', l2='下步道', tname='斜坡',
               note='上 // 下',
               marked=[('br1', '62°', R), ('tr2', '?', B)],
               caption='兩平行步道被斜坡穿過')
quad('fC4q3.png', 'kite', diagonals=True, O_label=True,
     diag_labels={'AC': '80', 'BD': '50'},
     caption='箏形風箏，骨架 80、50 互相垂直')
quad('fC4q4.png', 'para',
     side_labels={'AB': '8', 'CD': '8', 'BC': '5', 'AD': '5'},
     ticks=[('AB', 1, GREEN), ('CD', 1, GREEN), ('BC', 2, PURPLE),
            ('AD', 2, PURPLE)],
     angle_at={'A': '60°', 'B': '120°'}, diagonals=True, O_label=True,
     caption='ABCD：AB=CD=8、BC=AD=5，判斷形狀')

print('全部圖檔產生完成')
