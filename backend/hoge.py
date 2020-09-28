import time

from libs.node import TemplateNode, BatchNode, Statement
from libs.session import WorkSession

if __name__=="__main__":
    t11 = TemplateNode("template11")
    t12 = TemplateNode("template12")
    b1 = BatchNode("batch1", [t11, t12], statement=Statement.WHILE, cond=("lcnt","<",2))
    t21 = TemplateNode("template21")
    t22 = TemplateNode("template22")
    b2 = BatchNode("batch2", [t21, t22], statement=Statement.WHILE, cond=("lcnt","<",3))
    b3 = BatchNode("batch3", [b1, b2], statement=Statement.WHILE, cond=("cnt","<",2))
    b3.scan()

    #print(vars(b3))

    ws = WorkSession("worker", "project", b3)
    #ws = WorkSession("worker", "project", t)
    ns = None
    while (ns := ws.get_next_template_node_session(ns)):
        print("######", ns.node.name)
        time.sleep(0.1)
    else:
        ws.finish()

    ns = ws.root_ns
    while ns:
        print(ns.id, ns.node.name)
        ns = ns.next
