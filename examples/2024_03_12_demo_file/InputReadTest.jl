using Gridap
using GridapGmsh 
using Gmsh


model = GmshDiscreteModel("testfiles/model_v4.msh")
#model = GmshDiscreteModel("TutorialFiles/modelFromGATutorial.msh")

#writevtk(model,"res") 
order = 1
reffe = ReferenceFE(lagrangian,Float64,order)
V0 = TestFESpace(model,reffe;conformity=:H1,dirichlet_tags="sides")
g(x) = 2.0
Ug = TrialFESpace(V0,g)

degree = 2
Ω = Triangulation(model)
dΩ = Measure(Ω,degree)

neumanntags = ["circle","triangle","square"]
Γ = BoundaryTriangulation(model,tags=neumanntags)
dΓ = Measure(Γ,degree)


f(x) = 1.0
h(x) = 3.0
a(u,v) = ∫( ∇(v)⋅∇(u) )*dΩ
b(v) = ∫( v*f )*dΩ + ∫( v*h )*dΓ

op = AffineFEOperator(a,b,Ug,V0)

ls = LUSolver()
solver = LinearFESolver(ls)

uh = solve(solver,op)

writevtk(Ω,"results_og",cellfields=["uh"=>uh])
